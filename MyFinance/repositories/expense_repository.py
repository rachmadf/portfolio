"""
==========================================================
MyFinance

Expense Repository

Responsibilities
----------------
- SQLite data access
- Row-to-domain model mapping
- Master data retrieval
- Header insertion
- Validation helper methods

No business logic.
No transaction orchestration.
==========================================================
"""

from __future__ import annotations

from typing import List

from database import get_cursor

from models.expense_models import (
    Store,
    PaymentMethod,
    ExpenseCategory,
    ExpenseTransaction,
)


class ExpenseRepository:
    """
    Stateless repository responsible for expense-related
    SQLite operations.
    """

    # ======================================================
    # Mapping Helpers
    # ======================================================

    @staticmethod
    def _map_store(row) -> Store:
        """
        Convert SQLite row into Store object.
        """

        return Store(
            store_id=row["store_id"],
            store_name=row["store_name"],
            # created_at=row["created_at"],
        )

    @staticmethod
    def _map_category(row) -> ExpenseCategory:
        """
        Convert SQLite row into ExpenseCategory object.
        """

        return ExpenseCategory(
            category_id=row["category_id"],
            category_name=row["category_name"],
            # created_at=row["created_at"],
        )

    @staticmethod
    def _map_payment_method(row) -> PaymentMethod:
        """
        Convert SQLite row into PaymentMethod object.
        """

        return PaymentMethod(
            payment_method_id=row["payment_method_id"],
            payment_method_name=row["payment_method_name"],
            # created_at=row["created_at"],
        )

    # ======================================================
    # Master Data
    # ======================================================

    @staticmethod
    def get_all_stores() -> List[Store]:
        """
        Retrieve all stores ordered by name.
        """

        sql = """
            SELECT
                store_id,
                store_name
                
            FROM stores
            ORDER BY store_name
        """

        with get_cursor() as cursor:

            cursor.execute(sql)

            rows = cursor.fetchall()

        return [
            ExpenseRepository._map_store(row)
            for row in rows
        ]

    @staticmethod
    def get_all_categories() -> List[ExpenseCategory]:
        """
        Retrieve all expense categories ordered by name.
        """

        sql = """
            SELECT
                category_id,
                category_name
            FROM expense_categories
            ORDER BY category_name
        """

        with get_cursor() as cursor:

            cursor.execute(sql)

            rows = cursor.fetchall()

        return [
            ExpenseRepository._map_category(row)
            for row in rows
        ]

    @staticmethod
    def get_all_payment_methods() -> List[PaymentMethod]:
        """
        Retrieve all payment methods ordered by name.
        """

        sql = """
            SELECT
                payment_method_id,
                payment_method_name
            FROM payment_methods
            ORDER BY payment_method_name
        """

        with get_cursor() as cursor:

            cursor.execute(sql)

            rows = cursor.fetchall()

        return [
            ExpenseRepository._map_payment_method(row)
            for row in rows
        ]

    # ======================================================
    # Header CRUD
    # ======================================================

    @staticmethod
    def insert_transaction(
        connection,
        expense: ExpenseTransaction,
    ) -> int:
        """
        Insert an expense transaction header.

        Parameters
        ----------
        connection : sqlite3.Connection

        expense : ExpenseTransaction

        Returns
        -------
        int
            Newly created transaction ID.
        """

        sql = """
            INSERT INTO expense_transactions
            (
                expense_date,
                store_id,
                payment_method_id,
                receipt_number,
                notes,
                discount,
                grand_total
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?
            )
        """

        cursor = connection.cursor()

        # debug:
        print("expense.grand_total =", expense.grand_total)
        print("type =", type(expense.grand_total))

        values = (
            expense.expense_date,
            expense.store_id,
            expense.payment_method_id,
            expense.receipt_number,
            expense.notes,
            expense.discount,
            expense.grand_total,
        )

        print(values)
        print("Number of values =", len(values))

        print("Executing transaction insert...")

        try:
            cursor.execute(
                sql,
                (
                    expense.expense_date,
                    expense.store_id,
                    expense.payment_method_id,
                    expense.receipt_number,
                    expense.notes,
                    expense.discount,
                    expense.grand_total,
                ),
            )
            print("Transaction inserted successfully.")

        except Exception as e:
            print("FAILED HERE:", e)
            raise

        return cursor.lastrowid

    # ======================================================
    # Validation Helpers
    # ======================================================

    @staticmethod
    def store_exists(
        store_id: int,
    ) -> bool:
        """
        Check whether a store exists.
        """

        sql = """
            SELECT 1
            FROM stores
            WHERE store_id = ?
        """

        with get_cursor() as cursor:

            cursor.execute(
                sql,
                (store_id,),
            )

            return cursor.fetchone() is not None

    @staticmethod
    def category_exists(
        category_id: int,
    ) -> bool:
        """
        Check whether an expense category exists.
        """

        sql = """
            SELECT 1
            FROM expense_categories
            WHERE category_id = ?
        """

        with get_cursor() as cursor:

            cursor.execute(
                sql,
                (category_id,),
            )

            return cursor.fetchone() is not None

    @staticmethod
    def payment_method_exists(
        payment_method_id: int,
    ) -> bool:
        """
        Check whether a payment method exists.
        """

        sql = """
            SELECT 1
            FROM payment_methods
            WHERE payment_method_id = ?
        """

        with get_cursor() as cursor:

            cursor.execute(
                sql,
                (payment_method_id,),
            )

            return cursor.fetchone() is not None

    # ======================================================
    # Detail CRUD
    # ======================================================

    @staticmethod
    def insert_detail(
        connection,
        transaction_id: int,
        detail: ExpenseDetail,
    ) -> int:
        """
        Insert one expense detail.
        """

        sql = """
            INSERT INTO expense_details
            (
                transaction_id,
                category_id,
                item_name,
                -- brand,
                size,
                quantity,
                unit_price,
                subtotal
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?
            )
        """

        cursor = connection.cursor()

        cursor.execute(
            sql,
            (
                transaction_id,
                detail.category_id,
                detail.item_name,
                # detail.brand,
                detail.size,
                detail.quantity,
                detail.unit_price,
                detail.subtotal,
            ),
        )

        return cursor.lastrowid


    @staticmethod
    def get_details_by_transaction(
        transaction_id: int,
    ) -> List[ExpenseDetail]:
        """
        Retrieve all detail rows for one transaction.
        """

        sql = """
            SELECT
                detail_id,
                transaction_id,
                category_id,
                item_name,
                -- brand,
                size,
                quantity,
                unit_price,
                subtotal
                
            FROM expense_details
            WHERE transaction_id = ?
            ORDER BY detail_id
        """

        with get_cursor() as cursor:

            cursor.execute(
                sql,
                (transaction_id,),
            )

            rows = cursor.fetchall()

        details = []

        for row in rows:

            details.append(

                ExpenseDetail(

                    detail_id=row["detail_id"],
                    transaction_id=row["transaction_id"],
                    category_id=row["category_id"],
                    item_name=row["item_name"],
                    # brand=row["brand"],
                    size=row["size"],
                    quantity=row["quantity"],
                    unit_price=row["unit_price"],
                    subtotal=row["subtotal"],
                    # created_at=row["created_at"],

                )

            )

        return details


    @staticmethod
    def delete_details_by_transaction(
        connection,
        transaction_id: int,
    ) -> None:
        """
        Delete all details of one transaction.
        """

        sql = """
            DELETE
            FROM expense_details
            WHERE transaction_id = ?
        """

        cursor = connection.cursor()

        cursor.execute(
            sql,
            (transaction_id,),
        )

    # ======================================================
    # Transaction Query
    # ======================================================

    @staticmethod
    def get_transaction(
        transaction_id: int,
    ) -> ExpenseTransaction | None:
        """
        Retrieve one expense transaction.
        """

        sql = """
            SELECT
                transaction_id,
                expense_date,
                store_id,
                payment_method_id,
                receipt_number,
                notes,
                discount,
                grand_total
            FROM expense_transactions
            WHERE transaction_id = ?
        """

        with get_cursor() as cursor:

            cursor.execute(
                sql,
                (transaction_id,),
            )

            row = cursor.fetchone()

        if row is None:

            return None

        return ExpenseTransaction(

            transaction_id=row["transaction_id"],
            expense_date=row["expense_date"],
            store_id=row["store_id"],
            payment_method_id=row["payment_method_id"],
            receipt_number=row["receipt_number"],
            notes=row["notes"],
            discount=row["discount"],
            grand_total=row["grand_total"],
            # created_at=row["created_at"],

        )


    @staticmethod
    def get_complete_transaction(
        transaction_id: int,
    ) -> ExpenseTransaction | None:
        """
        Retrieve transaction together with details.
        """

        expense = ExpenseRepository.get_transaction(
            transaction_id
        )

        if expense is None:

            return None

        expense.details = ExpenseRepository.get_details_by_transaction(
            transaction_id
        )

        return expense

    # ======================================================
    # Header Update
    # ======================================================

    @staticmethod
    def update_transaction(
        connection,
        expense: ExpenseTransaction,
    ) -> None:
        """
        Update transaction header.
        """

        sql = """
            UPDATE expense_transactions
            SET
                expense_date = ?,
                store_id = ?,
                payment_method_id = ?,
                receipt_number = ?,
                notes = ?,
                discount = ?,
                grand_total = ?
            WHERE transaction_id = ?
        """

        cursor = connection.cursor()

        cursor.execute(

            sql,

            (
                expense.expense_date,
                expense.store_id,
                expense.payment_method_id,
                expense.receipt_number,
                expense.notes,
                expense.discount,
                expense.grand_total,
                expense.transaction_id,
            ),

        )

    # ======================================================
    # Header Delete
    # ======================================================

    @staticmethod
    def delete_transaction(
        connection,
        transaction_id: int,
    ) -> None:
        """
        Delete transaction header.
        """

        sql = """
            DELETE
            FROM expense_transactions
            WHERE transaction_id = ?
        """

        cursor = connection.cursor()

        cursor.execute(
            sql,
            (transaction_id,),
        )

    # ======================================================
    # Lookup Helpers
    # ======================================================

    @staticmethod
    def transaction_exists(
        transaction_id: int,
    ) -> bool:
        """
        Check whether transaction exists.
        """

        sql = """
            SELECT 1
            FROM expense_transactions
            WHERE transaction_id = ?
        """

        with get_cursor() as cursor:

            cursor.execute(
                sql,
                (transaction_id,),
            )

            return cursor.fetchone() is not None


    @staticmethod
    def receipt_exists(
        receipt_number: str,
    ) -> bool:
        """
        Check whether receipt number already exists.
        """

        sql = """
            SELECT 1
            FROM expense_transactions
            WHERE receipt_number = ?
        """

        with get_cursor() as cursor:

            cursor.execute(
                sql,
                (receipt_number,),
            )

            return cursor.fetchone() is not None

    # ===============================================
    # GET AVAILABLE YEAR
    # ===============================================
 
    @staticmethod
    def get_available_years():

        sql = """
            SELECT DISTINCT
                strftime('%Y', expense_date) AS year
            FROM expense_transactions
            ORDER BY year DESC
        """

        with get_cursor() as cursor:

            cursor.execute(sql)

            rows = cursor.fetchall()

        return [row["year"] for row in rows]




    # ===============================================
    # GET AVAILABLE MONTH
    # ===============================================
    @staticmethod
    def get_available_months(year):

        sql = """
            SELECT DISTINCT
                CAST(strftime('%m', expense_date) AS INTEGER) AS month
            FROM expense_transactions
            WHERE strftime('%Y', expense_date) = ?
            ORDER BY month
        """

        with get_cursor() as cursor:

            cursor.execute(sql, (str(year),))

            rows = cursor.fetchall()

        return [row["month"] for row in rows]


    # ===============================================
    # CALCULATE TOTAL EXPENSE BY MONTH & YEAR
    # ===============================================
    @staticmethod
    def get_total_expense(year: int, month: int) -> float:
        """
        Get total expense for a given year and month.
        """

        sql = """
            SELECT
                COALESCE(SUM(grand_total), 0) AS total_expense
            FROM expense_transactions
            WHERE strftime('%Y', expense_date) = ?
              AND strftime('%m', expense_date) = ?
        """

        with get_cursor() as cursor:

            cursor.execute(
                sql,
                (
                    str(year),
                    f"{month:02d}"
                )
            )

            row = cursor.fetchone()

        return row["total_expense"]

    # ===============================================
    # HIGHEST CATEGORY EXPENSE
    # ===============================================
    @staticmethod
    def get_highest_expense_category(year: int, month: int):
        """
        Get the category with the highest total expense
        for the specified year and month.
        """

        sql = """
            SELECT
                ec.category_name,
                SUM(ed.subtotal) AS total
            FROM expense_transactions et
            INNER JOIN expense_details ed
                ON et.transaction_id = ed.transaction_id
            INNER JOIN expense_categories ec
                ON ed.category_id = ec.category_id
            WHERE strftime('%Y', et.expense_date) = ?
              AND strftime('%m', et.expense_date) = ?
            GROUP BY
                ec.category_id,
                ec.category_name
            ORDER BY total DESC
            LIMIT 1
        """

        with get_cursor() as cursor:

            cursor.execute(
                sql,
                (
                    str(year),
                    f"{month:02d}"
                )
            )

            row = cursor.fetchone()

        if row is None:

            return {
                "highest_category": "-",
                "highest_category_total": 0
            }

        return {
            "highest_category": row["category_name"],
            "highest_category_total": row["total"]
        }


    # ===============================================
    # HIGHEST SINGLE TRANSACTION IN A MONTH
    # ===============================================
    @staticmethod
    def get_highest_transaction(year: int, month: int):
        """
        Get the highest expense transaction for the specified
        year and month.
        """

        sql = """
            SELECT
                s.store_name,
                et.grand_total
            FROM expense_transactions et
            INNER JOIN stores s
                ON et.store_id = s.store_id
            WHERE strftime('%Y', et.expense_date) = ?
              AND strftime('%m', et.expense_date) = ?
            ORDER BY et.grand_total DESC
            LIMIT 1
        """

        with get_cursor() as cursor:

            cursor.execute(
                sql,
                (
                    str(year),
                    f"{month:02d}"
                )
            )

            row = cursor.fetchone()

        if row is None:
            return {
                "highest_transaction_store": "-",
                "highest_transaction_amount": 0
            }

        return {
            "highest_transaction_store": row["store_name"],
            "highest_transaction_amount": row["grand_total"]
        }


    # ===============================================
    # AGGREGATION EXPENSE CATEGORY MONTHLY
    # ===============================================   
    @staticmethod
    def get_category_aggregation(year: int, month: int):
        """
        Return monthly expense aggregation by category.
        """

        sql = """
            SELECT
                ec.category_name,
                SUM(ed.subtotal) AS total
            FROM expense_transactions et

            INNER JOIN expense_details ed
                ON et.transaction_id = ed.transaction_id

            INNER JOIN expense_categories ec
                ON ed.category_id = ec.category_id

            WHERE strftime('%Y', et.expense_date) = ?
              AND strftime('%m', et.expense_date) = ?

            GROUP BY
                ec.category_id,
                ec.category_name

            ORDER BY total DESC
        """

        with get_cursor() as cursor:

            cursor.execute(
                sql,
                (
                    str(year),
                    f"{month:02d}"
                )
            )

            rows = cursor.fetchall()

        return [
            {
                "category": row["category_name"],
                "total": row["total"]
            }
            for row in rows
        ]

    # ===============================================
    # DAILY EXPENSE
    # ===============================================   
    @staticmethod
    def get_daily_expense_trend(year: str, month: str) -> list[dict]:
        """
        Return daily expense aggregation for the selected year and month.

        Returns:
            [
                {
                    "date": "2026-07-01",
                    "total": 250000
                },
                ...
            ]
        """

        sql = """
            SELECT
                DATE(et.expense_date) AS expense_date,
                SUM(ed.subtotal) AS total
            FROM expense_transactions et

            INNER JOIN expense_details ed
                ON et.transaction_id = ed.transaction_id

            WHERE
                strftime('%Y', et.expense_date) = ?
            AND
                strftime('%m', et.expense_date) = ?

            GROUP BY
                DATE(et.expense_date)

            ORDER BY
                DATE(et.expense_date);
        """

        with get_cursor() as cursor:

            cursor.execute(
                sql,
                (
                    str(year),
                    f"{month:02d}"
                )
            )

            rows = cursor.fetchall()

        return [
            {
                "date": row["expense_date"],
                "total": float(row["total"] or 0)
            }
            for row in rows
        ]

    # ===============================================
    # DETAILED DAILY EXPENSE
    # ===============================================
    @staticmethod
    def get_transaction_summary(year: int, month: int):
        """
        Return transaction summary for monthly expense report.
        """

        sql = """
            SELECT
                et.expense_date,
                s.store_name,
                ec.category_name,
                ed.item_name,
                ed.quantity,
                ed.unit_price,
                ed.subtotal
            FROM expense_transactions et

            INNER JOIN stores s
                ON et.store_id = s.store_id

            INNER JOIN expense_details ed
                ON et.transaction_id = ed.transaction_id

            INNER JOIN expense_categories ec
                ON ed.category_id = ec.category_id

            WHERE
                strftime('%Y', et.expense_date) = ?
            AND
                strftime('%m', et.expense_date) = ?

            ORDER BY
                et.expense_date DESC,
                et.transaction_id DESC,
                ed.detail_id ASC;
        """

        with get_cursor() as cursor:

            cursor.execute(
                sql,
                (
                    str(year),
                    f"{month:02d}"
                )
            )

            rows = cursor.fetchall()

        return [
            {
                "date": row["expense_date"],
                "store": row["store_name"],
                "category": row["category_name"],
                "item_name": row["item_name"],
                "quantity": row["quantity"],
                "unit_price": row["unit_price"],
                "subtotal": row["subtotal"]
            }
            for row in rows
        ]

    @staticmethod
    def get_transactions(connection, year, month):

        sql = """
            SELECT
                et.transaction_date,
                s.store_name,
                ec.category_name,
                ed.item_name,
                ed.quantity,
                ed.unit_price,
                ed.subtotal
            FROM expense_transactions et
            JOIN expense_details ed
                ON et.transaction_id = ed.transaction_id
            JOIN stores s
                ON et.store_id = s.store_id
            JOIN expense_categories ec
                ON ed.category_id = ec.category_id
            WHERE
                strftime('%Y', et.transaction_date)=?
                AND strftime('%m', et.transaction_date)=?
            ORDER BY et.transaction_date
        """

        cursor = connection.execute(
            sql,
            (
                str(year),
                f"{month:02d}"
            )
        )

        return cursor.fetchall()

    # ===============================================
    # DETAILED DAILY EXPENSE
    # ===============================================
    @staticmethod
    def get_items_by_category(category_id: int):

        sql = """
            SELECT
                d.item_name,
                d.unit_price AS last_price,
                t.usage_count

            FROM expense_details d

            INNER JOIN
            (
                SELECT
                    item_name,
                    COUNT(*) AS usage_count,
                    MAX(detail_id) AS last_detail_id

                FROM expense_details

                WHERE category_id = ?

                GROUP BY item_name

            ) t

                ON d.detail_id = t.last_detail_id

            ORDER BY
                t.usage_count DESC,
                d.item_name ASC
        """

        with get_cursor() as cursor:

            cursor.execute(sql, (category_id,))

            rows = cursor.fetchall()

        return [
            dict(row)
            for row in rows
        ]

    # ======================================================
    # Get Available Items
    # ======================================================
    @staticmethod
    def get_available_items(
        category_id=None,
        store_id=None,
        keyword=None
        ) -> list[dict]:

        sql = """
            SELECT

                d.item_name,

                d.category_id,

                c.category_name,

                t.store_id,

                s.store_name,

                d.unit_price,

                latest.total_transaction,

                t.expense_date AS last_purchase_date

            FROM expense_details d

            INNER JOIN expense_transactions t
                ON d.transaction_id = t.transaction_id

            INNER JOIN expense_categories c
                ON d.category_id = c.category_id

            INNER JOIN stores s
                ON t.store_id = s.store_id

            INNER JOIN
            (
                SELECT

                    d2.item_name,

                    d2.category_id,

                    t2.store_id,

                    MAX(d2.transaction_id) AS latest_transaction_id,

                    COUNT(*) AS total_transaction

                FROM expense_details d2

                INNER JOIN expense_transactions t2
                    ON d2.transaction_id = t2.transaction_id

                GROUP BY

                    d2.item_name,

                    d2.category_id,

                    t2.store_id

            ) latest

                ON d.transaction_id = latest.latest_transaction_id
               AND d.item_name = latest.item_name
               AND d.category_id = latest.category_id
               AND t.store_id = latest.store_id

            WHERE 1 = 1
        """

        params = []

        # --------------------------------------------------
        # Category Filter
        # --------------------------------------------------
        if category_id is not None:

            sql += """
                AND d.category_id = ?
            """

            params.append(category_id)

        # --------------------------------------------------
        # Store Filter
        # --------------------------------------------------
        if store_id is not None:

            sql += """
                AND t.store_id = ?
            """

            params.append(store_id)

        # --------------------------------------------------
        # Search Item
        # --------------------------------------------------
        if keyword:

            sql += """
                AND LOWER(d.item_name)
                    LIKE LOWER(?)
            """

            params.append(f"%{keyword}%")

        # --------------------------------------------------
        # Sorting
        # --------------------------------------------------
        sql += """

            ORDER BY

                d.item_name ASC

        """

        with get_cursor() as cursor:

            cursor.execute(sql, tuple(params))

            rows = cursor.fetchall()

        return [
            dict(row)
            for row in rows
        ]