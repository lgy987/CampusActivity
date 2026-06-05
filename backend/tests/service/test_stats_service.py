"""Statistics service tests - parameter validation only"""

import pytest
from app.services.stats_service import StatsService
from app.common.errors import BusinessError


class TestStatsServiceValidation:
    """Parameter validation tests"""
    
    def test_parse_period_week(self):
        """Test parse period 'week'"""
        from datetime import datetime, timedelta
        result = StatsService._parse_period("week")
        assert result is not None
        expected = datetime.utcnow() - timedelta(days=7)
        assert result.date() == expected.date()
    
    def test_parse_period_month(self):
        """Test parse period 'month'"""
        from datetime import datetime, timedelta
        result = StatsService._parse_period("month")
        expected = datetime.utcnow() - timedelta(days=30)
        assert result.date() == expected.date()
    
    def test_parse_period_all(self):
        """Test parse period 'all'"""
        result = StatsService._parse_period("all")
        assert result is None
    
    def test_parse_period_invalid(self):
        """Test invalid period"""
        with pytest.raises(BusinessError) as exc:
            StatsService._parse_period("invalid")
        assert "period" in str(exc.value).lower()
    
    def test_parse_period_empty(self):
        """Test empty string (defaults to all)"""
        result = StatsService._parse_period("")
        assert result is None
    
    def test_parse_period_none(self):
        """Test None value (defaults to all)"""
        result = StatsService._parse_period(None)
        assert result is None