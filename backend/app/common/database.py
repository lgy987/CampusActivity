"""
数据库会话管理模块

提供数据库连接和会话管理功能：
- 数据库引擎创建
- 会话工厂配置
- 上下文管理器风格的会话管理
"""
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import get_config

config = get_config()
engine = create_engine(config.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


@contextmanager
def db_session():
    """
    数据库会话上下文管理器
    
    使用 contextmanager 装饰器实现自动管理数据库会话的生命周期。
    确保会话在使用后正确提交或回滚，并最终关闭。
    
    异常处理:
        - 正常退出: 自动提交事务
        - 发生异常: 自动回滚事务
        - 最终: 自动关闭会话
    
    优点:
        - 自动管理事务边界
        - 避免手动 commit/rollback 遗漏
        - 确保会话被正确关闭
    
    Yields:
        Session: SQLAlchemy 会话对象
    
    Note:
        所有数据库操作都应该在 with 块内进行
        不要在会话关闭后使用查询结果（会触发 DetachedInstanceError）
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()