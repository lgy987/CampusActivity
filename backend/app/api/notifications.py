"""
通知与公告 API 路由模块

提供通知和公告管理相关的 API 接口：
- 获取我的通知列表
- 标记通知已读
- 发布系统公告（管理员）
- 获取系统公告
- 删除公告（管理员）
"""
from flask import Blueprint, request, g
from app.api.deps import get_json_data, require_auth, require_role
from app.common.response import success
from app.common.errors import BusinessError
from app.services.notification_service import NotificationService

bp = Blueprint('Notifications', __name__)

# ========== 个人通知 ==========
@bp.get('/notifications')
@require_auth()
def list_notifications():
    """
    获取我的通知列表
    
    支持分页和未读筛选
    
    Query Parameters:
        - page (int): 页码（默认1）
        - page_size (int): 每页数量（默认20，最大100）
        - unread (bool): 是否只显示未读（1/true/True）
    
    Returns:
        - total: 总记录数
        - page: 当前页码
        - page_size: 每页数量
        - unread_count: 未读通知数量
        - list: 通知列表
            - notification_id: 通知ID
            - title: 标题
            - content: 内容
            - type: 通知类型
            - related_id: 关联业务ID
            - is_read: 是否已读
            - created_at: 创建时间
    """
    params = request.args.to_dict()
    result = NotificationService.list_notifications(g.current_role, g.current_user_id, params)
    return success(result)


@bp.put('/notifications/<int:notification_id>/read')
@require_auth()
def mark_notification_read(notification_id):
    """
    标记通知已读
    
    将指定通知标记为已读状态
    
    Path Parameters:
        - notification_id (int): 通知ID
    
    Returns:
        message: 已标记为已读
    
    Raises:
        404: 通知不存在或不属于当前用户
    """
    NotificationService.mark_notification_read(g.current_role, g.current_user_id, notification_id)
    return success(None, message='已标记为已读')

# ========== 系统公告 ==========
@bp.post('/admin/announcements')
@require_auth()
@require_role('admin')
def create_announcement():
    """
    发布系统公告（管理员）
    
    管理员可以发布全站公告，公告会在指定时间范围内对外展示
    
    Request Body:
        - title (str): 公告标题（不超过50字符）
        - content (str): 公告正文
        - start_time (str, optional): 生效时间
            - 格式：%Y-%m-%d %H:%M:%S
            - 不传则立即生效
        - end_time (str, optional): 失效时间
            - 格式：%Y-%m-%d %H:%M:%S
            - 不传则默认30天后失效
    
    Returns:
        - announcement_id: 公告ID
    
    Raises:
        400: 标题/内容为空、标题过长、时间无效
    """
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
    """
    获取系统公告
    
    根据当前用户角色返回不同的数据：
    - 管理员：返回所有公告（不限有效期）
    - 普通用户/未登录：只返回有效期内的公告
    
    Returns:
        list: 公告列表
            - announcement_id: 公告ID
            - title: 标题
            - content: 内容
            - start_time: 生效时间
            - end_time: 失效时间
    """
    from app.api.deps import get_current_user
    role, user_id = get_current_user()
    
    if role == 'admin':
        result = NotificationService.list_announcements()
    else:
        result = NotificationService.list_valid_announcements()
    
    return success(result)


@bp.delete('/admin/announcements/<int:announcement_id>')
@require_auth()
@require_role('admin')
def delete_announcement(announcement_id):
    """
    删除公告（管理员）
    
    永久删除指定的系统公告
    
    Path Parameters:
        - announcement_id (int): 公告ID
    
    Returns:
        message: 公告删除成功
    
    Raises:
        404: 公告不存在
    """
    NotificationService.delete_announcement(announcement_id)
    return success(None, message='公告删除成功')