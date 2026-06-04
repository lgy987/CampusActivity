"""
报名服务模块

提供活动报名相关的完整功能：
- 报名活动（名额控制、重复报名检查、被拒绝后的冷却时间）
- 取消报名（延迟释放名额机制）
- 我的报名列表
- 活动报名人员列表（组织者视角）
- 拒绝报名（支持累计拒绝次数，两次后禁止报名）
- 报名数据统计
"""
from datetime import datetime, timedelta
from collections import Counter
from app.common.database import db_session
from app.common.errors import BusinessError
from app.common.serializers import dt
from app.services.notification_service import NotificationService
from models import Activity, Registration, User, Checkin

class RegistrationService:
    """
    报名服务类
    
    提供活动报名相关的业务逻辑：
    - 报名/取消报名
    - 名额管理（延迟释放机制）
    - 拒绝报名（累计次数，两次禁止）
    - 报名数据统计
    """

    ACTIVE_STATUSES = ('registered', 're_registered')
    # ========== 私有辅助方法 ==========
    @staticmethod
    def _now():
        """获取当前 UTC 时间"""
        return datetime.utcnow()

    @staticmethod
    def _active_count(session, activity_id):
        """
        计算有效报名人数
        
        有效报名包括：
        - 状态为 registered/re_registered 的记录
        - 状态为 cancelled 但名额还未释放的记录（slot_release_at > now）
        
        Args:
            session: 数据库会话
            activity_id (int): 活动ID
        
        Returns:
            int: 有效报名人数
        """
        now = datetime.utcnow()
    
        return session.query(Registration).filter(
        Registration.activity_id == activity_id,
        (
            (Registration.status.in_(RegistrationService.ACTIVE_STATUSES)) |
            ((Registration.status == 'cancelled') & (Registration.slot_release_at > now))
        )
        ).count()

    @staticmethod
    def _refresh_participants(session, activity):
        """
        刷新活动的当前参与人数
        
        处理已过期的取消报名（释放名额），然后重新计算有效报名数
        
        Args:
            session: 数据库会话
            activity: Activity 对象
        """
        now = datetime.utcnow()
    
        expired_regs = session.query(Registration).filter(
            Registration.activity_id == activity.id,
            Registration.status == 'cancelled',
            Registration.slot_release_at <= now
        ).all()
    
        for reg in expired_regs:
            reg.slot_release_at = None
        active_count = session.query(Registration).filter(
        Registration.activity_id == activity.id,
        (
            (Registration.status.in_(RegistrationService.ACTIVE_STATUSES)) |
            ((Registration.status == 'cancelled') & (Registration.slot_release_at > now))
        )
    ).count()
        activity.current_participants = active_count

    @staticmethod
    def _remaining_slots(session, activity):
        """
        计算剩余名额
        
        Args:
            session: 数据库会话
            activity: Activity 对象
        
        Returns:
            int: 剩余名额（不小于0）
        """
        RegistrationService._refresh_participants(session, activity)
        return max(activity.max_participants - activity.current_participants, 0)
    # ========== 核心业务方法 ==========
    @staticmethod
    def register(user_id, activity_id):
        """
        报名活动
        
        流程：
        1. 验证活动状态和报名截止时间
        2. 检查是否还有剩余名额
        3. 检查用户报名状态：
           - 已报名：拒绝重复报名
           - 被拒绝两次：禁止再次报名
           - 被拒绝一次：检查10分钟冷却期
           - 已取消：重新激活报名
           - 新用户：创建报名记录
        4. 发送报名成功通知
        
        Args:
            user_id (int): 用户ID
            activity_id (int): 活动ID
        
        Returns:
            dict: 包含 registration_id, status, remaining_slots
        
        Raises:
            BusinessError: 活动不存在、不可报名、名额已满、重复报名等
        """
        now = RegistrationService._now()

        with db_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity:
                raise BusinessError('活动不存在', code=404, status_code=404)
            if activity.status not in ('open', 'edit_pending'):
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
        """
        取消报名
        
        取消后名额不会立即释放，而是有2分钟延迟释放
        
        流程：
        1. 验证活动是否存在
        2. 验证取消截止时间
        3. 验证用户是否已报名
        4. 设置状态为 cancelled，设置延迟释放时间
        5. 发送取消通知
        
        Args:
            user_id (int): 用户ID
            activity_id (int): 活动ID
        
        Returns:
            dict: 包含 release_time 的字典
        
        Raises:
            BusinessError: 活动不存在、取消已截止、尚未报名
        """
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
        return {'release_time': dt(release_time)}

    @staticmethod
    def get_my_registrations(user_id, params):
        """
        获取我的报名列表
        
        只显示有效报名（registered/re_registered）
        支持筛选：活动名称、活动ID、分类、开始日期、校区
        
        Args:
            user_id (int): 用户ID
            params (dict): 查询参数
                - page: 页码
                - page_size: 每页数量
                - name: 活动名称（模糊匹配）
                - activity_id: 活动ID
                - category_id: 分类ID
                - start_date: 开始日期
                - campus: 校区
        
        Returns:
            dict: 分页的报名列表，包含签到状态
        """
        page = max(int(params.get('page', 1)), 1)
        page_size = min(max(int(params.get('page_size', 20)), 1), 100)
        activity_name = params.get('name', '').strip()
        activity_id = params.get('activity_id')
        category_id = params.get('category_id')
        start_date = params.get('start_date')
        campus = params.get('campus', '').strip()

        with db_session() as session:
            query = session.query(Registration).join(
                Activity, Registration.activity_id == Activity.id
            ).filter(
                Registration.user_id == user_id
            )
            query = query.filter(Registration.status.in_(('registered', 're_registered')))
            if activity_name:
                query = query.filter(Activity.name.contains(activity_name))
            if activity_id:
                try:
                    query = query.filter(Activity.id == int(activity_id))
                except ValueError:
                    pass
            if category_id:
                try:
                    query = query.filter(Activity.category_id == int(category_id))
                except ValueError:
                    pass
            if start_date:
                from datetime import datetime
                try:
                    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                except ValueError:
                    pass
                query = query.filter(Activity.start_time >= start_date_obj)
            if campus:
                query = query.filter(Activity.campus == campus)

            query = query.order_by(Registration.registration_time.desc())
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
        """
        获取活动报名人员列表（组织者视角）
        
        返回报名人员信息、签到情况、统计数据
        
        Args:
            organizer_id (int): 组织者ID
            activity_id (int): 活动ID
            params (dict): 查询参数
                - page: 页码
                - page_size: 每页数量
                - gender: 性别筛选
                - college: 学院筛选
                - grade: 年级筛选
                - major: 专业筛选
        
        Returns:
            dict: 分页的报名人员列表和统计数据
        """
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
            ).filter(
                Registration.activity_id == activity_id,
                Registration.status.in_(('registered', 're_registered'))  
            )

            for field in ['gender', 'college', 'grade', 'major']:
                value = params.get(field)
                if value:
                    query = query.filter(getattr(User, field) == value)

            total = query.count()
            all_rows = query.all()

            active_rows = all_rows
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
        """
        拒绝报名（组织者）
        
        拒绝逻辑：
        - 第1次拒绝：状态变为 rejected
        - 第2次拒绝：状态变为 blocked（永久禁止报名）
        - 每次拒绝增加 reject_count
        
        Args:
            organizer_id (int): 组织者ID
            registration_id (int): 报名记录ID
            reason (str): 拒绝原因
        
        Returns:
            dict: 包含 new_status 和 reject_count
        
        Raises:
            BusinessError: 报名记录不存在、无权操作、没有有效报名
        """
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
        """
        获取活动数据统计（组织者）
        
        返回报名人数统计、签到人数、按性别/学院/年级/专业分布
        
        Args:
            organizer_id (int): 组织者ID
            activity_id (int): 活动ID
        
        Returns:
            dict: 统计数据
        """
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
        