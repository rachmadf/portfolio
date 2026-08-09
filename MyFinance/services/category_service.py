# category_service.py

from __future__ import annotations
import json
import calendar
from database import get_cursor
from datetime import datetime
from typing import Any, Dict, List

from database import transaction
from repositories.category_repository import CategoryRepository
from models.category_models import Category


class CategoryService:

    # ======================================================
    # Get All Categories
    # ======================================================
    @staticmethod
    def get_all():

        return CategoryRepository.get_all()


    # ======================================================
    # Get Category By ID
    # ======================================================
    @staticmethod
    def get_by_id(category_id: int):

        return CategoryRepository.get_by_id(category_id)


    # ======================================================
    # Check Category Name Exists
    # ======================================================
    @staticmethod
    def exists_by_name(category_name: str):

        return CategoryRepository.exists_by_name(category_name)


    # ======================================================
    # Create Category
    # ======================================================
    @staticmethod
    def create(category: ExpenseCategory):

        if CategoryRepository.exists_by_name(category.category_name):
            raise ValueError("Category name already exists.")

        return CategoryRepository.insert(category)


    # ======================================================
    # Update Category
    # ======================================================
    @staticmethod
    def update(category: ExpenseCategory):

        existing = CategoryRepository.get_by_id(category.category_id)

        if existing is None:
            raise ValueError("Category not found.")

        return CategoryRepository.update(category)


    # ======================================================
    # Delete Category
    # ======================================================
    @staticmethod
    def delete(category_id: int):

        existing = CategoryRepository.get_by_id(category_id)

        if existing is None:
            raise ValueError("Category not found.")

        return CategoryRepository.delete(category_id)

    # get_all_categories()

    # add_category()

    # update_category()

    # delete_category()