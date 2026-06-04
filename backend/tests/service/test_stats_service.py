"""?????? - ????????????"""

import pytest
from app.services.stats_service import StatsService
from app.common.errors import BusinessError

class TestStatsServiceValidation:
    """??????"""
    
    def test_parse_period_week(self):
        """???? week ??"""
        from datetime import datetime, timedelta
        result = StatsService._parse_period("week")
        assert result is not None
        expected = datetime.utcnow() - timedelta(days=7)
        assert result.date() == expected.date()
    
    def test_parse_period_month(self):
        """???? month ??"""
        from datetime import datetime, timedelta
        result = StatsService._parse_period("month")
        expected = datetime.utcnow() - timedelta(days=30)
        assert result.date() == expected.date()
    
    def test_parse_period_all(self):
        """???? all ??"""
        result = StatsService._parse_period("all")
        assert result is None
    
    def test_parse_period_invalid(self):
        """??????"""
        with pytest.raises(BusinessError) as exc:
            StatsService._parse_period("invalid")
        # ?? in ????
        assert "period" in str(exc.value).lower() or "??" in str(exc.value)
    
    def test_parse_period_empty(self):
        """???????? all?"""
        result = StatsService._parse_period("")
        assert result is None
    
    def test_parse_period_none(self):
        """?? None ????? all?"""
        result = StatsService._parse_period(None)
        assert result is None
