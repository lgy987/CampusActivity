import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import get_config
from models import Base, Admin, Category


# 获取数据库配置
config = get_config()
engine = create_engine(config.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)


def seed_categories(session):
    """初始化分类数据"""
    categories = [
        (1, "学术类", 0, 1, 1),
        (2, "文体类", 0, 1, 2),
        (3, "志愿服务", 0, 1, 3),
        (4, "职业发展", 0, 1, 4),
        (5, "社交活动", 0, 1, 5),
        (6, "培训讲座", 0, 1, 6),
        (7, "其他", 0, 1, 7),
        (101, "讲座", 1, 2, 1),
        (102, "竞赛", 1, 2, 2),
        (103, "沙龙", 1, 2, 3),
        (201, "运动会", 2, 2, 1),
        (202, "体育比赛", 2, 2, 2),
        (203, "文艺演出", 2, 2, 3),
        (301, "志愿服务", 3, 2, 1),
        (302, "募捐活动", 3, 2, 2),
        (401, "招聘会", 4, 2, 1),
        (402, "职业讲座", 4, 2, 2),
        (403, "实习分享", 4, 2, 3),
        (404, "简历指导", 4, 2, 4),
        (501, "联谊活动", 5, 2, 1),
        (502, "社团招新", 5, 2, 2),
        (503, "迎新活动", 5, 2, 3),
        (601, "技能培训", 6, 2, 1),
        (602, "语言培训", 6, 2, 2),
        (603, "考试辅导", 6, 2, 3),
    ]
    
    existing_ids = {row[0] for row in session.query(Category.id).all()}
    
    for category_id, name, parent_id, level, sort_order in categories:
        if category_id not in existing_ids:
            session.add(Category(
                id=category_id,
                name=name,
                parent_id=parent_id,
                level=level,
                sort_order=sort_order
            ))


def seed_admin(session):
    """初始化超级管理员账号"""
    admin = session.query(Admin).filter(Admin.admin_no == "000001").first()
    
    if not admin:
        admin = Admin(
            admin_no="000001",
            email="admin@example.com",
            password=generate_password_hash(os.getenv("ADMIN_PASSWORD", "Admin123456")),
            username="超级管理员",
            role="super_admin",
            status="active",
        )
        session.add(admin)
        print("超级管理员账号创建成功")
    else:
        print("超级管理员账号已存在")


def init_database():
    """初始化数据库"""
    print("开始初始化数据库...")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功")
    
    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # 初始化分类数据
        seed_categories(session)
        print("分类数据初始化完成")
        
        # 初始化超级管理员
        seed_admin(session)
        print("超级管理员初始化完成")
        
        # 提交所有更改
        session.commit()
        print("数据库初始化完成！")
        
    except Exception as e:
        session.rollback()
        print(f"初始化失败: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    init_database()