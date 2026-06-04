"""
签到服务模块

提供活动签到相关的完整功能：
- 签到码生成（组织者）
- 扫码签到（普通用户）
- 手动签到（组织者）
- 签到记录查询
- 签到统计
"""
import random
import string
from datetime import datetime, timedelta
from app.common.database import db_session
from app.common.errors import BusinessError
from app.common.serializers import dt
from app.services.notification_service import NotificationService
from models import Activity, ActivityCheckinCode, Registration, Checkin, User


class CheckinService:
    """
    签到服务类
    
    提供活动签到相关的业务逻辑：
    - 签到码生成与管理
    - 扫码签到（用户自助）
    - 手动签到（组织者辅助）
    - 签到数据统计
    """

    ACTIVE_STATUSES = ('registered', 're_registered')
     # ========== 私有辅助方法 ==========
    @staticmethod
    def _now():
        """获取当前 UTC 时间"""
        return datetime.utcnow()

    @staticmethod
    def _random_code():
        """
        生成6位随机签到码
        
        包含大写字母和数字，共 36^6 种组合
        
        Returns:
            str: 6位随机字符串
        """
        alphabet = string.ascii_uppercase + string.digits
        return ''.join(random.choice(alphabet) for _ in range(6))

    @staticmethod
    def _checkin_window_error(activity):
        """
        检查签到时间窗口
        
        签到时间窗口：活动开始前30分钟 到 活动结束时间
        
        Args:
            activity: Activity 对象
        
        Returns:
            str: 错误信息，如果窗口有效则返回 None
        """
        now = CheckinService._now()
        if now < activity.start_time - timedelta(minutes=30):
            return '签到尚未开始'
        if now > activity.end_time:
            return '签到已结束'
        return None

    # ========== 核心业务方法 ==========
    @staticmethod
    def get_checkin_code(organizer_id, activity_id):
        """
        获取签到码（组织者）
        
        如果活动没有签到码，会自动生成一个
        
        Args:
            organizer_id (int): 组织者ID
            activity_id (int): 活动ID
        
        Returns:
            dict: 包含 checkin_code 的字典
        
        Raises:
            BusinessError: 活动不存在、无权操作
        """
        with db_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity:
                raise BusinessError('活动不存在', code=404, status_code=404)
            if activity.organizer_id != organizer_id:
                raise BusinessError('无权管理该活动', code=403, status_code=403)

            row = session.query(ActivityCheckinCode).filter(ActivityCheckinCode.activity_id == activity_id).first()
            if not row:
                row = ActivityCheckinCode(activity_id=activity_id, checkin_code=CheckinService._random_code())
                session.add(row)
                session.flush()

            return {'checkin_code': row.checkin_code}


    @staticmethod
    def checkin(user_id, activity_id, checkin_code):
        """
        签到码签到（普通用户）
        
        用户通过输入签到码自助签到
        
        流程：
        1. 验证活动存在
        2. 验证签到码正确
        3. 验证签到时间窗口（开始前30分钟到结束后）
        4. 验证用户已报名
        5. 验证未重复签到
        6. 创建签到记录
        7. 发送签到成功通知
        
        Args:
            user_id (int): 用户ID
            activity_id (int): 活动ID
            checkin_code (str): 签到码
        
        Returns:
            dict: 包含 checkin_id 和 checkin_time
        
        Raises:
            BusinessError: 活动不存在、签到码错误、时间窗口无效、未报名、重复签到
        """
        with db_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity:
                raise BusinessError('活动不存在', code=404, status_code=404)

            code = session.query(ActivityCheckinCode).filter(ActivityCheckinCode.activity_id == activity.id).first()
            if not code or code.checkin_code.upper() != checkin_code.upper():
                raise BusinessError('签到码错误')

            if error := CheckinService._checkin_window_error(activity):
                raise BusinessError(error)

            registration = session.query(Registration).filter(
                Registration.activity_id == activity.id,
                Registration.user_id == user_id
            ).first()
            if not registration or registration.status not in CheckinService.ACTIVE_STATUSES:
                raise BusinessError('只有已报名用户可以签到')

            existing = session.query(Checkin).filter(
                Checkin.activity_id == activity.id,
                Checkin.user_id == user_id
            ).first()
            if existing:
                raise BusinessError('你已完成签到，请勿重复签到')

            checkin = Checkin(
                activity_id=activity.id,
                user_id=user_id,
                checkin_method='code'
            )
            session.add(checkin)
            session.flush()

            NotificationService.create_notification(
                session, 'user', user_id,
                '签到成功',
                f'你已成功签到 {activity.name}。',
                'checkin_result', activity.id
            )

            return {'checkin_id': checkin.id, 'checkin_time': dt(checkin.checkin_time)}

    @staticmethod
    def manual_checkin(organizer_id, activity_id, student_id):
        """
        手动签到（组织者）
        
        组织者通过学号帮助用户完成签到
        
        流程：
        1. 验证活动存在且有权限
        2. 验证用户存在
        3. 验证用户已报名
        4. 验证未重复签到
        5. 创建手动签到记录
        6. 发送签到成功通知
        
        Args:
            organizer_id (int): 组织者ID
            activity_id (int): 活动ID
            student_id (str): 用户学号
        
        Returns:
            dict: 包含 user_id 和 checkin_time
        
        Raises:
            BusinessError: 活动不存在、无权操作、用户不存在、未报名、重复签到
        """
        with db_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity:
                raise BusinessError('活动不存在', code=404, status_code=404)
            if activity.organizer_id != organizer_id:
                raise BusinessError('无权管理该活动', code=403, status_code=403)

            user = session.query(User).filter(User.student_id == student_id, User.status == 'active').first()
            if not user:
                raise BusinessError('用户不存在', code=404, status_code=404)

            registration = session.query(Registration).filter(
                Registration.activity_id == activity_id,
                Registration.user_id == user.id
            ).first()
            if not registration or registration.status not in CheckinService.ACTIVE_STATUSES:
                raise BusinessError('该用户未有效报名')

            existing = session.query(Checkin).filter(
                Checkin.activity_id == activity_id,
                Checkin.user_id == user.id
            ).first()
            if existing:
                raise BusinessError('该用户已完成签到')

            checkin = Checkin(
                activity_id=activity_id,
                user_id=user.id,
                checkin_method='manual',
                operator_id=organizer_id
            )
            session.add(checkin)
            session.flush()

            NotificationService.create_notification(
                session, 'user', user.id,
                '手动签到成功',
                f'组织者为 {activity.name} 完成手动签到。',
                'checkin_result', activity.id
            )

            return {'user_id': user.id, 'checkin_time': dt(checkin.checkin_time)}

    @staticmethod
    def get_my_checkins(user_id, params):
        """
        获取我的签到记录
        
        返回用户的历史签到记录，按签到时间倒序
        
        Args:
            user_id (int): 用户ID
            params (dict): 查询参数
                - page: 页码（默认1）
                - page_size: 每页数量（默认20，最大100）
        
        Returns:
            dict: 分页的签到记录列表
        """
        page = max(int(params.get('page', 1)), 1)
        page_size = min(max(int(params.get('page_size', 20)), 1), 100)

        with db_session() as session:
            query = session.query(Checkin).join(
                Activity, Checkin.activity_id == Activity.id
            ).filter(
                Checkin.user_id == user_id
            ).order_by(Checkin.checkin_time.desc())

            total = query.count()
            rows = query.offset((page - 1) * page_size).limit(page_size).all()

            data = [{
                'activity_id': row.activity_id,
                'activity_name': row.activity.name,
                'activity_start_time': dt(row.activity.start_time),
                'checkin_time': dt(row.checkin_time),
                'checkin_method': row.checkin_method
            } for row in rows]

            return {'total': total, 'list': data}

    @staticmethod
    def get_checkin_stats(organizer_id, activity_id):
        """
        获取活动签到情况（组织者）
        
        返回签到统计数据和详细列表：
        - 总报名人数
        - 已签到人数
        - 未签到人数
        - 签到率
        - 已签到用户列表（含签到时间、方式）
        - 未签到用户列表（含报名时间）
        
        Args:
            organizer_id (int): 组织者ID
            activity_id (int): 活动ID
        
        Returns:
            dict: 签到统计信息
        
        Raises:
            BusinessError: 活动不存在、无权操作
        """
        with db_session() as session:
            activity = session.get(Activity, activity_id)
            if not activity:
                raise BusinessError('活动不存在', code=404, status_code=404)
            if activity.organizer_id != organizer_id:
                raise BusinessError('无权管理该活动', code=403, status_code=403)

            total_registered = session.query(Registration).filter(
                Registration.activity_id == activity_id,
                Registration.status.in_(CheckinService.ACTIVE_STATUSES)
            ).count()

            checkins = session.query(Checkin).join(
                User, Checkin.user_id == User.id
            ).filter(
                Checkin.activity_id == activity_id
            ).order_by(Checkin.checkin_time.desc()).all()

            checked_user_ids = [c.user_id for c in checkins]
            checked_in = len(checkins)

            not_checked_query = session.query(Registration).join(
                User, Registration.user_id == User.id
            ).filter(
                Registration.activity_id == activity_id,
                Registration.status.in_(CheckinService.ACTIVE_STATUSES)
            )
            if checked_user_ids:
                not_checked_query = not_checked_query.filter(~Registration.user_id.in_(checked_user_ids))
            not_checked = not_checked_query.order_by(Registration.registration_time.asc()).all()

            return {
                'total_registered': total_registered,
                'checked_in': checked_in,
                'not_checked_in': max(total_registered - checked_in, 0),
                'checkin_rate': f'{(checked_in / total_registered * 100) if total_registered else 0:.2f}%',
                'checkin_list': [{
                    'user_id': c.user.id,
                    'student_id': c.user.student_id,
                    'username': c.user.username,
                    'college': c.user.college,     
                    'major': c.user.major,          
                    'grade': c.user.grade,  
                    'checkin_time': dt(c.checkin_time),
                    'checkin_method': c.checkin_method
                } for c in checkins],
                'notCheckedIn': [{
                    'user_id': r.user.id,
                    'student_id': r.user.student_id,
                    'username': r.user.username,
                    'registration_time': dt(r.registration_time)
                } for r in not_checked]
            }