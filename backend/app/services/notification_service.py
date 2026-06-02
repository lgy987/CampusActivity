from datetime import datetime, timedelta
from app.common.database import db_session
from app.common.errors import BusinessError
from app.common.serializers import dt
from models import Notification, Announcement


class NotificationService:
    """通知服务"""

    @staticmethod
    def create_notification(session, receiver_type, receiver_id, title, content, type_, related_id):
        """创建通知（内部方法）"""
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
        """获取我的通知列表"""
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
        """标记通知已读"""
        with db_session() as session:
            notification = session.get(Notification, notification_id)
            if not notification or notification.receiver_type != role or notification.receiver_id != user_id:
                raise BusinessError('通知不存在', code=404, status_code=404)
            notification.is_read = True

    @staticmethod
    def _parse_datetime(value):
        """解析日期时间字符串"""
        if not value:
            return None
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        raise BusinessError('日期时间格式无效')

    @staticmethod
    def create_announcement(admin_id, title, content, start_time, end_time):
        """发布系统公告（管理员）"""
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
        """获取所有系统公告（管理员用，不过滤有效期）"""
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
        """获取有效期内的系统公告（普通用户用）"""
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
        """删除公告"""
        with db_session() as session:
            announcement = session.get(Announcement, announcement_id)
            if not announcement:
                raise BusinessError('公告不存在', code=404, status_code=404)
            session.delete(announcement)