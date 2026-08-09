# category_repository.py

from __future__ import annotations
from typing import List
from database import get_cursor

class CategoryRepository:

	# ======================================================
    # Get All Category Row
    # ======================================================
    @staticmethod
    def get_all() -> List[dict]:

        sql = """
            SELECT
                category_id,
                category_name,
                is_active
            FROM expense_categories
            ORDER BY category_name
        """

        with get_cursor() as cursor:

            cursor.execute(sql)

            rows = cursor.fetchall()

        return [
            dict(row)
            for row in rows
        ]

	# ======================================================
    # 
    # ======================================================
    @staticmethod
    def get_by_id(category_id: int):

        sql = """
            SELECT
                category_id,
                category_name,
                is_active
            FROM expense_categories
            WHERE category_id = ?
        """

        with get_cursor() as cursor:

            cursor.execute(sql, (category_id,))

            row = cursor.fetchone()

        return dict(row) if row else None

	# ======================================================
    # Mapping Helpers
    # ======================================================
    @staticmethod
    def exists_by_name(category_name: str) -> bool:

        sql = """
            SELECT 1
            FROM expense_categories
            WHERE LOWER(category_name) = LOWER(?)
            LIMIT 1
        """

        with get_cursor() as cursor:

            cursor.execute(sql, (category_name,))

            return cursor.fetchone() is not None

	# ======================================================
    # Mapping Helpers
    # ======================================================
    # @staticmethod
    # insert(category)

	# ======================================================
    # Mapping Helpers
    # ======================================================
    # @staticmethod
    # update(category)

	# ======================================================
    # Mapping Helpers
    # ======================================================
    # @staticmethod
    # delete(category_id)