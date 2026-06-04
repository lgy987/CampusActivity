from app.common.serializers import dt
from datetime import datetime

class TestDtSerializer:
    def test_dt_with_datetime(self):
        dt_obj = datetime(2026, 6, 4, 14, 30, 0)
        result = dt(dt_obj)
        assert "2026-06-04" in result
    
    def test_dt_with_none(self):
        assert dt(None) is None
    
    def test_dt_with_string(self):
        assert dt("2026-06-04") == "2026-06-04"
