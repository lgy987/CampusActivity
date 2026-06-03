from flask import Blueprint
from app.common.response import success
from app.services.category_service import CategoryService

bp = Blueprint('Categories', __name__)


@bp.get('')
def get_categories():
    """获取分类列表 """
    result = CategoryService.get_category_tree()
    return success(result)