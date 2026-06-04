"""
活动 API 路由模块（组织者视角）

提供活动管理相关的 API 接口：
- 创建活动（草稿）
- 提交审核
- 更新活动
- 删除活动
- 获取我发布的活动列表
- 公开的活动列表和详情查询
"""
from flask import Blueprint, request, g
from app.api.deps import get_json_data, require_auth, require_role
from app.common.response import success
from app.common.errors import BusinessError
from app.services.activity_service import ActivityService

bp = Blueprint('Activities', __name__)


@bp.post('/organizer/activities')
@require_auth()
@require_role('organizer')
def create_activity():
    """
    创建活动（草稿）
    
    组织者创建活动，初始状态为 draft（草稿）
    只有审核通过的组织者才能创建活动
    
    Request Body:
        - name (str): 活动名称
        - category_id (int): 分类ID
        - start_time (str): 开始时间
        - end_time (str): 结束时间
        - campus (str): 校区（良乡/中关村）
        - location (str): 具体地点
        - max_participants (int): 人数上限
        - registration_deadline (str): 报名截止时间
        - cancel_deadline (str): 取消报名截止时间
        - description (str): 活动描述
    
    Returns:
        - activity_id: 活动ID
        - status: 活动状态（draft）
    
    Raises:
        403: 组织者账号未审核通过
        404: 活动分类不存在
    """
    data = get_json_data()
    try:
        result = ActivityService.create_activity(g.current_user_id, data)
        return success(result, message='活动创建成功')
    except BusinessError as e:
        return e.to_response()


@bp.post('/organizer/activities/<int:activity_id>/submit')
@require_auth()
@require_role('organizer')
def submit_activity(activity_id):
    """
    提交活动审核
    
    将活动提交给管理员审核
    - 草稿状态 → pending（待审核）
    - 已发布状态 → edit_pending（修改待审核）
    
    Path Parameters:
        - activity_id (int): 活动ID
    
    Returns:
        - activity_id: 活动ID
        - status: 新状态（pending/edit_pending）
    
    Raises:
        403: 无权操作（不是自己的活动）
        404: 活动不存在
    """
    try:
        result = ActivityService.submit_activity(g.current_user_id, activity_id)
        return success(result, message='已提交审核')
    except BusinessError as e:
        return e.to_response()


@bp.get('/activities')
def list_activities():
    """
    获取活动列表（公开接口）
    
    支持分页和多条件筛选，默认只显示可见状态的活动
    
    Query Parameters:
        - page (int): 页码（默认1）
        - page_size (int): 每页数量（默认20，最大100）
        - keyword (str): 关键词搜索（活动名称）
        - category_id (int): 分类ID
        - campus (str): 校区筛选
        - status (str): 状态筛选（逗号分隔）
        - organizer_id (int): 组织者ID筛选
        - start_date (str): 开始日期（格式：YYYY-MM-DD）
    
    Returns:
        - total: 总记录数
        - page: 当前页码
        - page_size: 每页数量
        - list: 活动列表
    """
    params = request.args.to_dict()
    result = ActivityService.list_activities(params)
    return success(result)


@bp.get('/activities/<int:activity_id>')
def get_activity_detail(activity_id):
    """
    获取活动详情（公开接口）
    
    根据当前登录用户角色返回不同内容：
    - 未登录用户：只看到已发布的活动
    - 普通用户：额外看到报名状态和签到状态
    - 组织者/管理员：edit_pending 状态时看到修改内容
    
    Path Parameters:
        - activity_id (int): 活动ID
    
    Returns:
        dict: 活动详细信息
    """
    from app.api.deps import get_current_user
    role, user_id = get_current_user()
    result = ActivityService.get_detail(activity_id, role, user_id)
    return success(result)


@bp.put('/organizer/activities/<int:activity_id>')
@require_auth()
@require_role('organizer')
def update_activity(activity_id):
    """
    更新活动
    
    根据活动状态决定更新方式：
    - 草稿/待审核/已拒绝：直接更新
    - 已发布状态：创建修改记录，进入二次审核
    
    限制：
    - 活动开始前1小时内不可修改
    - 已发布活动的人数限制只能增加不能减少
    
    Path Parameters:
        - activity_id (int): 活动ID
    
    Request Body:
        与创建活动相同
    
    Returns:
        - activity_id: 活动ID
        - status: 活动状态
    
    Raises:
        403: 无权操作
        400: 修改时间过期、人数限制减少等
    """
    data = get_json_data()
    try:
        result = ActivityService.update_activity(g.current_user_id, activity_id, data)
        return success(result, message='活动更新成功')
    except BusinessError as e:
        return e.to_response()


@bp.delete('/organizer/activities/<int:activity_id>')
@require_auth()
@require_role('organizer')
def delete_activity(activity_id):
    """
    删除活动
    
    彻底删除活动及所有相关数据（报名、签到、签到码、修改记录）
    删除前会发送通知给所有已报名用户
    
    限制：
    - 活动已开始不可删除
    - 活动开始前1小时内不可删除
    
    Path Parameters:
        - activity_id (int): 活动ID
    
    Returns:
        message: 删除成功提示
    
    Raises:
        403: 无权操作
        400: 活动已开始或开始前1小时内
    """
    try:
        ActivityService.delete_activity(g.current_user_id, activity_id)
        return success(None, message='活动已删除，已通知所有报名用户')
    except BusinessError as e:
        return e.to_response()


@bp.get('/organizer/activities')
@require_auth()
@require_role('organizer')
def get_my_activities():
    """
    获取我发布的活动列表（组织者专用）
    
    返回当前组织者创建的所有活动
    支持分页和筛选
    
    Query Parameters:
        - page (int): 页码（默认1）
        - page_size (int): 每页数量（默认20，最大100）
        - keyword (str): 关键词搜索（活动名称）
        - category_id (int): 分类ID
        - campus (str): 校区筛选
        - status (str): 状态筛选（逗号分隔）
        - start_date (str): 开始日期（格式：YYYY-MM-DD）
    
    Returns:
        - total: 总记录数
        - page: 当前页码
        - page_size: 每页数量
        - list: 活动列表
    """
    params = request.args.to_dict()
    result = ActivityService.get_my_activities(g.current_user_id, params)
    return success(result)