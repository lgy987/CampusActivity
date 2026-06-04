"""
序列化工具模块

提供数据格式转换和序列化函数：
- datetime 对象格式化为 ISO 8601 格式
"""
from datetime import datetime, timezone

def dt(value):
    """
    格式化日期时间为 ISO 8601 格式（UTC）
    
    将 datetime 对象转换为前端友好的标准格式
    主要用于 API 响应中的时间字段序列化
    
    Args:
        value: 待格式化的值，通常为 datetime 对象或 None
    
    Returns:
        str | None: 
            - 如果是 datetime 对象：返回 ISO 8601 格式的字符串
            - 如果是 None：返回 None
            - 其他类型：返回 str(value)
    
    格式说明:
        - 输出格式: "YYYY-MM-DDTHH:MM:SSZ"
        - 示例: "2026-05-31T10:42:44Z"
        - 末尾的 'Z' 表示 UTC 时区
    
    Note:
        该函数确保所有时间输出为 UTC 时区
        前端可以直接使用 new Date() 解析
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat().replace('+00:00', 'Z')
    return str(value)