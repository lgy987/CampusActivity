from datetime import datetime, timezone

def dt(value):
    """格式化日期时间为 ISO 格式（UTC）"""
    if value is None:
        return None
    if isinstance(value, datetime):
        # 确保是 UTC 时间
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        # 返回 ISO 格式，如 "2026-05-31T10:42:44Z"
        return value.isoformat().replace('+00:00', 'Z')
    return str(value)