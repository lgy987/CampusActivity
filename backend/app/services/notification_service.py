"""
通知服务模块

提供系统通知和公告的管理功能：
- 通知创建、列表查询、已读标记
- 公告创建、列表查询、删除
- 支持管理员和普通用户不同视角
"""
from datetime import datetime, timedelta
from app.common.database import db_session
from app.common.errors import BusinessError
from app.common.serializers import dt
from models import Notification, Announcement


class NotificationService:
    """
    通知服务类
    
    提供系统通知和公告的业务逻辑：
    - 创建通知（供其他服务调用）
    - 获取通知列表（支持分页和未读筛选）
    - 标记通知已读
    - 发布系统公告
    - 获取公告列表（区分管理员/普通用户）
    - 删除公告
    """
    # ========== 通知相关 ==========
    @staticmethod
    def create_notification(session, receiver_type, receiver_id, title, content, type_, related_id):
        """
        创建通知（内部方法）
        
        供其他服务模块调用，如：
        - 活动审核结果通知
        - 报名结果通知
        - 活动变更通知
        - 活动提醒通知
        
        Args:
            session: 数据库会话
            receiver_type (str): 接收者类型：user / organizer
            receiver_id (int): 接收者ID
            title (str): 通知标题
            content (str): 通知内容
            type_ (str): 通知类型
                - registration_result: 报名结果
                - activity_audit_result: 活动审核结果
                - activity_change: 活动变更
                - violation_result: 违规处理
                - activity_reminder: 活动提醒
                - organizer_audit_result: 组织者审核结果
            related_id (int): 关联业务ID（活动ID、报名ID等）
        
        Returns:
            Notification: 创建的通知对象
        """
        notification = Notification(
            receiver_type=receiver_type,
            receiver_id=receiver_id,
            title=title,
            content=content,
            type=type_,
            related_id=related_id,
            is_read=False
        )
        session.add(notification)
        return notification

    @staticmethod
    def list_notifications(role, user_id, params):
        """
        获取我的通知列表
        
        支持分页和未读筛选
        
        Args:
            role (str): 用户角色：user / organizer
            user_id (int): 用户ID
            params (dict): 查询参数
                - page: 页码（默认1）
                - page_size: 每页数量（默认20，最大100）
                - unread: 是否只显示未读（1/true/True）
        
        Returns:
            dict: 分页的通知列表，包含未读数量
        """
        page = max(int(params.get('page', 1)), 1)
        page_size = min(max(int(params.get('page_size', 20)), 1), 100)
        only_unread = params.get('unread') in ('1', 'true', 'True')

        with db_session() as session:
            query = session.query(Notification).filter(
                Notification.receiver_type == role,
                Notification.receiver_id == user_id
            )

            if only_unread:
                query = query.filter(Notification.is_read.is_(False))

            unread_count = session.query(Notification).filter(
                Notification.receiver_type == role,
                Notification.receiver_id == user_id,
                Notification.is_read.is_(False)
            ).count()

            total = query.count()
            rows = query.order_by(
                Notification.created_at.desc(),
                Notification.id.desc()
            ).offset((page - 1) * page_size).limit(page_size).all()

            return {
                'total': total,
                'page': page,
                'page_size': page_size,
                'unread_count': unread_count,
                'list': [{
                    'notification_id': row.id,
                    'title': row.title,
                    'content': row.content,
                    'type': row.type,
                    'related_id': row.related_id,
                    'is_read': row.is_read,
                    'created_at': dt(row.created_at)
                } for row in rows]
            }

    @staticmethod
    def mark_notification_read(role, user_id, notification_id):
        """
        标记通知已读
        
        Args:
            role (str): 用户角色
            user_id (int): 用户ID
            notification_id (int): 通知ID
        
        Raises:
            BusinessError: 通知不存在或不属于当前用户
        """
        with db_session() as session:
            notification = session.get(Notification, notification_id)
            if not notification or notification.receiver_type != role or notification.receiver_id != user_id:
                raise BusinessError('Notification not found', code=404, status_code=404)
            notification.is_read = True
    # ========== 公告相关 ==========
    @staticmethod
    def _parse_datetime(value):
        """
        解析日期时间字符串（内部方法）
        
        支持多种格式：
        - %Y-%m-%d %H:%M:%S
        - %Y-%m-%dT%H:%M:%S
        - %Y-%m-%d
        
        Args:
            value: 日期时间字符串
        
        Returns:
            datetime: 解析后的 datetime 对象
        
        Raises:
            BusinessError: 日期格式无效
        """
        if not value:
            return None
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        raise BusinessError('Invalid datetime format')

    @staticmethod
    def create_announcement(admin_id, title, content, start_time, end_time):
        """
        发布系统公告（管理员）
        
        公告会在 start_time 到 end_time 期间对外展示
        
        Args:
            admin_id (int): 发布管理员ID
            title (str): 公告标题（不超过50字符）
            content (str): 公告正文
            start_time (str): 生效时间（格式：%Y-%m-%d %H:%M:%S）
            end_time (str): 失效时间（格式：%Y-%m-%d %H:%M:%S）
        
        Returns:
            dict: 包含 announcement_id 的字典
        
        Raises:
            BusinessError: 标题/内容为空、标题过长、时间无效
        """
        if not title or not content:
            raise BusinessError('标题和内容不能为空', code=400)
        if len(title) > 50:
            raise BusinessError('标题不能超过50字符', code=400)
        start = start_time and datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') or datetime.utcnow()
        end = end_time and datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') or (start + timedelta(days=30))
        if end <= start:
            raise BusinessError('公告结束时间必须晚于开始时间', code=400)

        with db_session() as session:
            announcement = Announcement(
                admin_id=admin_id,
                title=title,
                content=content,
                start_time=start,
                end_time=end
            )
            session.add(announcement)
            session.flush()
            return {'announcement_id': announcement.id}


    @staticmethod
    def list_announcements():
        """
        获取所有系统公告（管理员用）
        
        不过滤有效期，返回所有公告（按创建时间倒序）
        
        Returns:
            list: 公告列表
        """
        with db_session() as session:
            rows = session.query(Announcement).order_by(Announcement.created_at.desc()).all()
        
            return [{
                'announcement_id': row.id,
                'title': row.title,
                'content': row.content,
                'start_time': dt(row.start_time),
                'end_time': dt(row.end_time)
            } for row in rows]
        
    @staticmethod
    def list_valid_announcements():
        """
        获取有效期内的系统公告（普通用户用）
        
        只返回当前时间在 start_time 和 end_time 之间的公告
        
        Returns:
            list: 有效期内的公告列表
        """
        current_time = datetime.utcnow()
        with db_session() as session:
            rows = session.query(Announcement).filter(
                Announcement.start_time <= current_time,
                Announcement.end_time >= current_time
            ).order_by(Announcement.created_at.desc()).all()
            return [{
                'announcement_id': row.id,
                'title': row.title,
                'content': row.content,
                'start_time': dt(row.start_time),
                'end_time': dt(row.end_time)
            } for row in rows]
        
    @staticmethod
    def delete_announcement(announcement_id):
        """
        删除公告（管理员）
        
        Args:
            announcement_id (int): 公告ID
        
        Raises:
            BusinessError: 公告不存在
        """
        with db_session() as session:
            announcement = session.get(Announcement, announcement_id)
            if not announcement:
                raise BusinessError('Announcement not found', code=404, status_code=404)
            session.delete(announcement)