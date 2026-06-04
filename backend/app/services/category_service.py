"""
分类服务模块

提供活动分类的树形结构管理功能
"""
from app.common.database import db_session
from models import Category
class CategoryService:
    """
    分类服务类
    
    提供活动分类相关的业务逻辑：
    - 获取分类树形结构（用于前端展示）
    - 支持多级分类（目前支持两级）
    """
    @staticmethod
    def get_category_tree():
        """
        获取分类树形结构
        
        将数据库中扁平存储的分类数据转换为树形结构，
        便于前端渲染级联选择器或树形菜单。
        
        分类结构示例：
        - 学术类 (id:1, level:1)
          - 讲座 (id:101, parent_id:1, level:2)
          - 竞赛 (id:102, parent_id:1, level:2)
          - 沙龙 (id:103, parent_id:1, level:2)
        - 文体类 (id:2, level:1)
          - 运动会 (id:201, parent_id:2, level:2)
          - ...
        
        构建逻辑：
        1. 查询所有分类，按 sort_order 排序
        2. 创建分类ID到节点的映射
        3. 遍历所有分类：
           - 如果 parent_id == 0，添加到根节点列表
           - 否则，找到父节点并添加到其 children 数组
        
        Returns:
            list: 树形结构的分类列表，每个节点包含：
                - id: 分类ID
                - name: 分类名称
                - level: 层级（1-一级，2-二级）
                - sort_order: 排序序号
                - children: 子分类列表
        """
        with db_session() as session:
            categories = session.query(Category).order_by(Category.sort_order).all()

            category_map = {c.id: {'id': c.id, 'name': c.name, 'level': c.level, 'sort_order': c.sort_order, 'children': []} for c in categories}
            tree = []

            for c in categories:
                node = category_map[c.id]
                if c.parent_id == 0:
                    tree.append(node)
                else:
                    parent = category_map.get(c.parent_id)
                    if parent:
                        parent['children'].append(node)

            return tree