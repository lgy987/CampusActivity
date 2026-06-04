"""
分类 API 路由模块

提供活动分类管理相关的 API 接口：
- 获取分类树形结构

分类用于活动的前端筛选和展示
"""
from flask import Blueprint
from app.common.response import success
from app.services.category_service import CategoryService

bp = Blueprint('Categories', __name__)


@bp.get('')
def get_categories():
    """
    获取分类列表（树形结构）
    
    返回两级分类的树形结构，便于前端渲染级联选择器或树形菜单。
    预设分类包括：
    - 学术类（讲座、竞赛、沙龙）
    - 文体类（运动会、体育比赛、文艺演出）
    - 志愿服务（志愿服务、募捐活动）
    - 职业发展（招聘会、职业讲座、实习分享、简历指导）
    - 社交活动（联谊活动、社团招新、迎新活动）
    - 培训讲座（技能培训、语言培训、考试辅导）
    - 其他
    
    Returns:
        list: 树形结构的分类列表，每个节点包含：
            - id: 分类ID
            - name: 分类名称
            - level: 层级（1-一级分类，2-二级分类）
            - sort_order: 排序序号
            - children: 子分类列表（二级分类）
    """
    result = CategoryService.get_category_tree()
    return success(result)