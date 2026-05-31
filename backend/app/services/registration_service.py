from datetime import datetime, timedelta
from collections import Counter
from app.common.database import db_session
from app.common.errors import BusinessError
from app.common.serializers import dt
from app.services.notification_service import NotificationService
from models import Activity, Registration, User, Checkin
from threading import Timer

class RegistrationService:
    """报名服务"""

    ACTIVE_STATUSES = ('registered', 're_registered')

    @staticmethod
    def _now():
        return datetime.utcnow()

    @staticmethod
    def _active_count(session, activity_id):
        return session.query(Registration).filter(
            Registration.activity_id == activity_id,
            Registration.status.in_(RegistrationService.ACTIVE_STATUSES)
        ).count()

    @staticmethod
    def _refresh_participants(session, activity):
        activity.current_participants = RegistrationService._active_count(session, activity.id)

    @staticmethod
    def _remaining_slots(session, activity):
        RegistrationService._refresh_participants(session, activity)
        return max(activity.max_participants - activity.current_participants, 0)

    @staticmethod
    def register(user_id, activity_id):
        """报名活动"""
        now = RegistrationService._now()

        with db_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity:
                raise BusinessError('活动不存在', code=404, status_code=404)
            if activity.status != 'open':
                raise BusinessError('当前活动不可报名')
            if now > activity.registration_deadline:
                raise BusinessError('报名已截止')
            if RegistrationService._remaining_slots(session, activity) <= 0:
                raise BusinessError('当前活动报名人数已满')

            row = session.query(Registration).filter(
                Registration.activity_id == activity.id,
                Registration.user_id == user_id
            ).first()

            if row:
                if row.status in RegistrationService.ACTIVE_STATUSES:
                    raise BusinessError('你已报名该活动，请勿重复报名')
                if row.status == 'blocked' or row.reject_count >= 2:
                    raise BusinessError('你已被这活动拒绝两次，不可再报名！')
                if row.status == 'rejected':
                    if row.last_reject_time and now < row.last_reject_time + timedelta(minutes=10):
                        raise BusinessError('报名被拒绝后10分钟内不可再次报名')
                    row.status = 're_registered'
                elif row.status == 'cancelled':
                    row.status = 'registered'
                row.registration_time = now
                row.slot_release_at = None
                row.reject_reason = None
            else:
                row = Registration(
                    activity_id=activity.id,
                    user_id=user_id,
                    status='registered'
                )
                session.add(row)
                session.flush()

            session.flush()
            RegistrationService._refresh_participants(session, activity)

            NotificationService.create_notification(
                session, 'user', user_id,
                '报名成功',
                f'你已成功报名 {activity.name}。',
                'registration_result', activity.id
            )

            return {
                'registration_id': row.id,
                'status': row.status,
                'remaining_slots': RegistrationService._remaining_slots(session, activity)
            }

    @staticmethod
    def cancel(user_id, activity_id):
        """取消报名"""
        now = RegistrationService._now()

        with db_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity:
                raise BusinessError('活动不存在', code=404, status_code=404)
            if now > activity.cancel_deadline:
                raise BusinessError('取消报名已截止')

            row = session.query(Registration).filter(
                Registration.activity_id == activity_id,
                Registration.user_id == user_id
            ).first()

            if not row or row.status not in RegistrationService.ACTIVE_STATUSES:
                raise BusinessError('你尚未报名该活动')

            release_time = now + timedelta(minutes=2)
            row.status = 'cancelled'
            row.slot_release_at = release_time
            session.flush()

            NotificationService.create_notification(
                session, 'user', user_id,
                '报名取消',
                f'你取消了对 {activity.name} 的报名。',
                'registration_result', activity.id
            )

            def release_slot():
                with db_session() as bg_session:
                    bg_activity = bg_session.get(Activity, activity_id)
                    if bg_activity:
                        # 重新计算报名人数
                        active_count = bg_session.query(Registration).filter(
                            Registration.activity_id == activity_id,
                            Registration.status.in_(RegistrationService.ACTIVE_STATUSES)
                        ).count()
                        bg_activity.current_participants = active_count
                        bg_session.commit()
        
            timer = Timer(120.0, release_slot)  # 2分钟后执行
            timer.daemon = True
            timer.start()
        return {'release_time': dt(release_time)}

    @staticmethod
    def get_my_registrations(user_id, params):
        """获取我的报名列表"""
        page = max(int(params.get('page', 1)), 1)
        page_size = min(max(int(params.get('page_size', 20)), 1), 100)

        with db_session() as session:
            query = session.query(Registration).join(
                Activity, Registration.activity_id == Activity.id
            ).filter(
                Registration.user_id == user_id
            ).order_by(Registration.registration_time.desc())

            total = query.count()
            rows = query.offset((page - 1) * page_size).limit(page_size).all()

            data = []
            for row in rows:
                checkin = session.query(Checkin).filter(
                    Checkin.activity_id == row.activity_id,
                    Checkin.user_id == row.user_id
                ).first()
                data.append({
                    'registration_id': row.id,
                    'activity_id': row.activity_id,
                    'activity_name': row.activity.name,
                    'start_time': dt(row.activity.start_time),
                    'end_time': dt(row.activity.end_time),
                    'location': row.activity.location,
                    'registration_time': dt(row.registration_time),
                    'status': row.status,
                    'checkin_status': 'checked' if checkin else 'not_checked',
                    'checkin_time': dt(checkin.checkin_time) if checkin else None
                })

            return {'total': total, 'page': page, 'page_size': page_size, 'list': data}

    @staticmethod
    def get_activity_registrations(organizer_id, activity_id, params):
        """获取活动报名人员列表（组织者）"""
        page = max(int(params.get('page', 1)), 1)
        page_size = min(max(int(params.get('page_size', 20)), 1), 100)

        with db_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity:
                raise BusinessError('活动不存在', code=404, status_code=404)
            if activity.organizer_id != organizer_id:
                raise BusinessError('无权管理该活动', code=403, status_code=403)

            query = session.query(Registration).join(
                User, Registration.user_id == User.id
            ).filter(Registration.activity_id == activity_id)

            # 筛选
            for field in ['gender', 'college', 'grade', 'major']:
                value = params.get(field)
                if value:
                    query = query.filter(getattr(User, field) == value)
            status = params.get('status')
            if status:
                query = query.filter(Registration.status == status)

            total = query.count()
            all_rows = query.all()

            # 统计
            active_rows = [r for r in all_rows if r.status in RegistrationService.ACTIVE_STATUSES]
            active_user_ids = [r.user_id for r in active_rows]
            total_checked = session.query(Checkin).filter(
                Checkin.activity_id == activity_id,
                Checkin.user_id.in_(active_user_ids)
            ).count() if active_user_ids else 0

            stats = {
                'total_registered': len(active_rows),
                'total_checked': total_checked,
                'remaining_slots': max(activity.max_participants - len(active_rows), 0),
                'by_gender': dict(Counter(r.user.gender for r in active_rows)),
                'by_college': dict(Counter(r.user.college for r in active_rows)),
                'by_grade': dict(Counter(r.user.grade for r in active_rows)),
                'by_major': dict(Counter(r.user.major for r in active_rows))
            }

            rows = query.order_by(Registration.registration_time.desc()).offset((page - 1) * page_size).limit(page_size).all()

            list_data = []
            for row in rows:
                checkin = session.query(Checkin).filter(
                    Checkin.activity_id == activity_id,
                    Checkin.user_id == row.user_id
                ).first()
                list_data.append({
                    'registration_id': row.id,
                    'user_id': row.user.id,
                    'student_id': row.user.student_id,
                    'gender': row.user.gender,
                    'college': row.user.college,
                    'major': row.user.major,
                    'grade': row.user.grade,
                    'registration_time': dt(row.registration_time),
                    'status': row.status,
                    'reject_reason': row.reject_reason,
                    'checkin_status': 'checked' if checkin else 'not_checked'
                })

            return {'total': total, 'statistics': stats, 'list': list_data}

    @staticmethod
    def reject_registration(organizer_id, registration_id, reason):
        """拒绝报名"""
        with db_session() as session:
            row = session.get(Registration, registration_id)
            if not row:
                raise BusinessError('报名记录不存在', code=404, status_code=404)

            activity = session.get(Activity, row.activity_id)
            if not activity or activity.organizer_id != organizer_id:
                raise BusinessError('无权操作', code=403, status_code=403)

            if row.status not in RegistrationService.ACTIVE_STATUSES:
                raise BusinessError('该用户没有有效报名记录')

            row.reject_count += 1
            row.last_reject_time = RegistrationService._now()
            row.reject_reason = reason
            row.status = 'blocked' if row.reject_count >= 2 else 'rejected'
            session.flush()

            RegistrationService._refresh_participants(session, activity)

            NotificationService.create_notification(
                session, 'user', row.user_id,
                '报名拒绝',
                f'你的ID为{activity.id}名字为{activity.name}的报名被拒绝了。原因: {reason}',
                'registration_result', activity.id
            )

            return {'new_status': row.status, 'reject_count': row.reject_count}

    @staticmethod
    def get_registration_stats(organizer_id, activity_id):
        """获取活动数据统计"""
        with db_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity:
                raise BusinessError('活动不存在', code=404, status_code=404)
            if activity.organizer_id != organizer_id:
                raise BusinessError('无权查看', code=403, status_code=403)

            rows = session.query(Registration).filter(Registration.activity_id == activity_id).all()
            active_rows = [r for r in rows if r.status in RegistrationService.ACTIVE_STATUSES]
            active_user_ids = [r.user_id for r in active_rows]

            total_checked = session.query(Checkin).filter(
                Checkin.activity_id == activity_id,
                Checkin.user_id.in_(active_user_ids)
            ).count() if active_user_ids else 0

            return {
                'total_registered': len(active_rows),
                'remaining_slots': max(activity.max_participants - len(active_rows), 0),
                'total_checked': total_checked,
                'by_gender': dict(Counter(r.user.gender for r in active_rows)),
                'by_college': dict(Counter(r.user.college for r in active_rows)),
                'by_grade': dict(Counter(r.user.grade for r in active_rows)),
                'by_major': dict(Counter(r.user.major for r in active_rows))
            }