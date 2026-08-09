from __future__ import annotations

from typing import List

from database import get_cursor
from models.store_models import Store


class StoreRepository:

	@staticmethod
	def get_all() -> List[dict]:

	    sql = """
	        SELECT
	            store_id,
	            store_name,
	            is_active
	        FROM stores
	        ORDER BY store_name
	    """

	    with get_cursor() as cursor:

	        cursor.execute(sql)

	        rows = cursor.fetchall()

	    return [
	        dict(row)
	        for row in rows
	    ]


	@staticmethod
	def get_by_id(store_id: int):

	    sql = """
	        SELECT
	            store_id,
	            store_name,
	            is_active
	        FROM stores
	        WHERE store_id = ?
	    """

	    with get_cursor() as cursor:

	        cursor.execute(sql, (store_id,))

	        row = cursor.fetchone()

	    return dict(row) if row else None


	@staticmethod
	def exists_by_name(store_name: str) -> bool:

	    sql = """
	        SELECT 1
	        FROM stores
	        WHERE LOWER(store_name) = LOWER(?)
	        LIMIT 1
	    """

	    with get_cursor() as cursor:

	        cursor.execute(sql, (store_name,))

	        return cursor.fetchone() is not None


	@staticmethod
	def insert(store: Store):

	    sql = """
	        INSERT INTO stores
	        (
	            store_name,
	            is_active
	        )
	        VALUES
	        (
	            ?,
	            ?
	        )
	    """

	    with get_cursor() as cursor:

	        cursor.execute(
	            sql,
	            (
	                store.store_name,
	                store.is_active
	            )
	        )

	        return cursor.lastrowid


	@staticmethod
	def update(store: Store):

	    sql = """
	        UPDATE stores
	        SET
	            store_name = ?,
	            is_active = ?
	        WHERE store_id = ?
	    """

	    with get_cursor() as cursor:

	        cursor.execute(
	            sql,
	            (
	                store.store_name,
	                store.is_active,
	                store.store_id
	            )
	        )

	        return cursor.rowcount


	@staticmethod
	def delete(store_id: int):

	    sql = """
	        DELETE FROM stores
	        WHERE store_id = ?
	    """

	    with get_cursor() as cursor:

	        cursor.execute(sql, (store_id,))

	        return cursor.rowcount