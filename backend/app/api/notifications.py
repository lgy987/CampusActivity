from flask import Blueprint, request, g
from app.api.deps import get_json_data, require_auth, require_role
from app.common.response import success
from app.common.errors import BusinessError
from app.services.notification_service import NotificationService

bp = Blueprint('Notifications', __name__)


@bp.get('/notifications')
@require_auth()
def list_notifications():
    """获取我的通知列表 """
    params = request.args.to_dict()
    result = NotificationService.list_notifications(g.current_role, g.current_user_id, params)
    return success(result)


@bp.put('/notifications/<int:notification_id>/read')
@require_auth()
def mark_notification_read(notification_id):
    """标记通知已读"""
    NotificationService.mark_notification_read(g.current_role, g.current_user_id, notification_id)
    return success(None, message='已标记为已读')


@bp.post('/admin/announcements')
@require_auth()
@require_role('admin')
def create_announcement():
    """发布系统公告（管理员）"""
    data = get_json_data()
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    if not title or not content:
        raise BusinessError('标题和内容不能为空', code=400)
    result = NotificationService.create_announcement(g.current_user_id, title, content, start_time, end_time)
    return success(result, message='公告发布成功')


@bp.get('/announcements')
def list_announcements():
    """获取系统公告（根据角色返回不同数据）"""
    # 获取当前用户信息（可选，未登录也可以）
    from app.api.deps import get_current_user
    role, user_id = get_current_user()
    
    if role == 'admin':
        # 管理员：返回所有公告
        result = NotificationService.list_announcements()
    else:
        # 普通用户或未登录用户：只返回有效期内的公告
        result = NotificationService.list_valid_announcements()
    
    return success(result)


@bp.delete('/admin/announcements/<int:announcement_id>')
@require_auth()
@require_role('admin')
def delete_announcement(announcement_id):
    """删除公告 （管理员）"""
    NotificationService.delete_announcement(announcement_id)
    return success(None, message='公告删除成功')