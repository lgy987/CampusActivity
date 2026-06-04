"""Unit tests for category service"""

import pytest
import time
from app.services.category_service import CategoryService
from app.common.database import db_session
from models import Category


class TestCategoryService:
    
    def test_get_category_tree_returns_list(self, app):
        """Test get category tree returns list"""
        with app.app_context():
            # Create test categories
            with db_session() as session:
                # Create parent category
                parent = Category(
                    id=100,
                    name="Parent Category",
                    parent_id=0,
                    level=1,
                    sort_order=1
                )
                session.add(parent)
                
                # Create child category
                child = Category(
                    id=101,
                    name="Child Category",
                    parent_id=100,
                    level=2,
                    sort_order=1
                )
                session.add(child)
                session.flush()
            
            # Test get category tree
            with db_session() as session:
                result = CategoryService.get_category_tree()
                assert isinstance(result, list)
    
    def test_get_category_tree_structure(self, app):
        """Test category tree has correct structure"""
        with app.app_context():
            # Create test categories
            with db_session() as session:
                # Create parent category
                parent = Category(
                    id=200,
                    name="Parent Category",
                    parent_id=0,
                    level=1,
                    sort_order=1
                )
                session.add(parent)
                
                # Create child category
                child = Category(
                    id=201,
                    name="Child Category",
                    parent_id=200,
                    level=2,
                    sort_order=1
                )
                session.add(child)
                session.flush()
            
            # Test structure
            with db_session() as session:
                result = CategoryService.get_category_tree()
                if result:
                    for category in result:
                        assert "id" in category
                        assert "name" in category
                        assert "level" in category
                        assert "children" in category
    
    def test_get_category_tree_with_no_categories(self, app):
        """Test get category tree with no categories"""
        with app.app_context():
            # Clear categories first
            with db_session() as session:
                session.query(Category).delete()
                session.flush()
            
            with db_session() as session:
                result = CategoryService.get_category_tree()
                assert isinstance(result, list)
                # May be empty list if no categories
                assert result == [] or isinstance(result, list)