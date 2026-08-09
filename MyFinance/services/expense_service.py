"""
==========================================================
MyFinance

Expense Service

Responsibilities
----------------
- Business logic
- Validation
- Model construction
- Transaction orchestration
- No SQL statements
==========================================================
"""

from __future__ import annotations

import json
import calendar

from database import get_cursor
from datetime import datetime
from typing import Any, Dict, List

from repositories.expense_repository import (
    ExpenseRepository,
)

from database import transaction

from models.expense_models import (
    ExpenseTransaction,
    ExpenseDetail,
    SaveExpenseResult,
)


class ExpenseService:
    """
    Business layer for expense transactions.
    """

    # =====================================================
    # Dropdown Data
    # =====================================================

    @staticmethod
    def load_expense_form() -> Dict[str, Any]:
        """
        Load all master data required by expense_add.html
        """

        return {

            "stores":
                ExpenseRepository.get_all_stores(),

            "categories":
                ExpenseRepository.get_all_categories(),

            "payment_methods":
                ExpenseRepository.get_all_payment_methods(),

        }

    # =====================================================
    # Validation
    # =====================================================

    @staticmethod
    def _validate_header(
        expense: ExpenseTransaction,
    ) -> None:
        """
        Validate transaction header.
        """

        if expense.expense_date is None:
            raise ValueError(
                "Expense date is required."
            )

        if not ExpenseRepository.store_exists(
            expense.store_id
        ):
            raise ValueError(
                "Invalid store."
            )

        if not ExpenseRepository.payment_method_exists(
            expense.payment_method_id
        ):
            raise ValueError(
                "Invalid payment method."
            )

        if expense.discount < 0:
            raise ValueError(
                "Discount cannot be negative."
            )

    @staticmethod
    def _validate_details(
        details: List[ExpenseDetail],
    ) -> None:
        """
        Validate all purchased items.
        """

        if len(details) == 0:

            raise ValueError(
                "At least one item is required."
            )

        for detail in details:

            if not ExpenseRepository.category_exists(
                detail.category_id
            ):
                raise ValueError(
                    f"Invalid category ID: {detail.category_id}"
                )

            if detail.item_name.strip() == "":
                raise ValueError(
                    "Item name cannot be empty."
                )

            if detail.quantity <= 0:
                raise ValueError(
                    "Quantity must be greater than zero."
                )

            if detail.unit_price < 0:
                raise ValueError(
                    "Unit price cannot be negative."
                )

    # =====================================================
    # Builders
    # =====================================================

    @staticmethod
    def _build_detail(
        item: Dict[str, Any],
    ) -> ExpenseDetail:
        """
        Convert JSON item into ExpenseDetail.
        """

        detail = ExpenseDetail(

            category_id=int(
                item["category_id"]
            ),

            item_name=item["item_name"],

            # brand=item.get(
            #     "brand",
            #     "",
            # ),

            size=item.get(
                "size",
                "",
            ),

            quantity=float(
                item["quantity"]
            ),

            unit_price=float(
                item["unit_price"]
            ),

        )

        detail.calculate_subtotal()

        return detail

    @staticmethod
    def _build_transaction(
        form,
    ) -> ExpenseTransaction:
        """
        Build ExpenseTransaction object from form data.
        """

        expense = ExpenseTransaction(

            expense_date=datetime.strptime(
                form["expense_date"],
                "%Y-%m-%d",
            ).date(),

            store_id=int(
                form["store_id"]
            ),

            payment_method_id=int(
                form["payment_method_id"]
            ),

            receipt_number=form.get(
                "receipt_number",
                "",
            ),

            notes=form.get(
                "notes",
                "",
            ),

            discount=float(
                form.get(
                    "discount",
                    0,
                )
            ),

        )

        detail_json = form.get(
            "expense_details",
            "[]",
        )

        items = json.loads(
            detail_json
        )

        for item in items:

            expense.add_detail(

                ExpenseService._build_detail(
                    item
                )

            )

        return expense

    # =====================================================
    # Calculation
    # =====================================================

    @staticmethod
    def _calculate_totals(
        expense: ExpenseTransaction,
    ) -> None:
        """
        Recalculate all totals.
        """

        for detail in expense.details:

            detail.calculate_subtotal()

        expense.calculate_total()

    # =====================================================
    # Save
    # =====================================================

    @staticmethod
    def save_expense(
        form,
    ) -> SaveExpenseResult:
        """
        Save a new expense transaction.
        """

        expense = ExpenseService._build_transaction(
            form
        )

        ExpenseService._calculate_totals(
            expense
        )

        ExpenseService._validate_header(
            expense
        )

        ExpenseService._validate_details(
            expense.details
        )

        with transaction() as connection:

            transaction_id = (
                ExpenseRepository.insert_transaction(
                    connection,
                    expense,
                )
            )

            for detail in expense.details:

                ExpenseRepository.insert_detail(
                    connection,
                    transaction_id,
                    detail,
                )

        return SaveExpenseResult(

            success=True,

            transaction_id=transaction_id,

            message="Expense saved successfully.",

        )

    # =====================================================
    # Update
    # =====================================================

    @staticmethod
    def update_expense(
        transaction_id: int,
        form,
    ) -> SaveExpenseResult:
        """
        Update an existing expense transaction.
        """

        expense = ExpenseService._build_transaction(
            form
        )

        expense.transaction_id = transaction_id

        ExpenseService._calculate_totals(
            expense
        )

        ExpenseService._validate_header(
            expense
        )

        ExpenseService._validate_details(
            expense.details
        )

        with transaction() as connection:

            ExpenseRepository.update_transaction(
                connection,
                expense,
            )

            ExpenseRepository.delete_details_by_transaction(
                connection,
                transaction_id,
            )

            for detail in expense.details:

                ExpenseRepository.insert_detail(
                    connection,
                    transaction_id,
                    detail,
                )

        return SaveExpenseResult(

            success=True,

            transaction_id=transaction_id,

            message="Expense updated successfully.",

        )

    # =====================================================
    # Query
    # =====================================================

    @staticmethod
    def get_expense(
        transaction_id: int,
    ) -> ExpenseTransaction | None:
        """
        Retrieve a complete expense transaction.
        """

        return ExpenseRepository.get_complete_transaction(
            transaction_id
        )

    # =====================================================
    # Delete
    # =====================================================

    @staticmethod
    def delete_expense(
        transaction_id: int,
    ) -> SaveExpenseResult:
        """
        Delete an expense transaction.
        """

        if not ExpenseRepository.transaction_exists(
            transaction_id
        ):

            return SaveExpenseResult(

                success=False,

                transaction_id=None,

                message="Expense transaction not found.",

            )

        with transaction() as connection:

            ExpenseRepository.delete_details_by_transaction(
                connection,
                transaction_id,
            )

            ExpenseRepository.delete_transaction(
                connection,
                transaction_id,
            )

        return SaveExpenseResult(

            success=True,

            transaction_id=transaction_id,

            message="Expense deleted successfully.",

        )

    # =====================================================
    # Utility
    # =====================================================

    @staticmethod
    def receipt_exists(
        receipt_number: str,
    ) -> bool:
        """
        Check whether a receipt number already exists.
        """

        return ExpenseRepository.receipt_exists(
            receipt_number
        )

    # =====================================================
    # GET MONTH NAME
    # =====================================================

    @staticmethod
    def get_report_filter():

        today = datetime.now()

        years = ExpenseRepository.get_available_years()

        selected_year = today.year

        if years and str(selected_year) not in years:
            selected_year = int(years[0])

        months = ExpenseRepository.get_available_months(
            selected_year
        )

        months = [
            {
                "value": month,
                "name": calendar.month_name[month]
            }
            for month in months
        ]

        selected_month = today.month

        if months:
            available = [m["value"] for m in months]

            if selected_month not in available:
                selected_month = months[0]["value"]

        total_expense = ExpenseRepository.get_total_expense(
            selected_year,
            selected_month
        )

        highest = ExpenseRepository.get_highest_expense_category(
            selected_year,
            selected_month
        )

        highest_transaction = ExpenseRepository.get_highest_transaction(
            selected_year,
            selected_month
        )

        category_summary = ExpenseRepository.get_category_aggregation(
            selected_year,
            selected_month
        )

        daily_trend = ExpenseRepository.get_daily_expense_trend(
            selected_year,
            selected_month
        )

        transactions = ExpenseRepository.get_transaction_summary(
            selected_year,
            selected_month
        )

        return {
            "years": years,
            "months": months,
            "selected_year": selected_year,
            "selected_month": selected_month,
            "total_expense": total_expense,
            "highest_category":
                highest["highest_category"],

            "highest_category_total":
                highest["highest_category_total"],

            "highest_transaction_store":
                highest_transaction["highest_transaction_store"],

            "highest_transaction_amount":
                highest_transaction["highest_transaction_amount"],

            "category_summary": category_summary,

            "daily_trend": daily_trend,

            "transactions": transactions
        }

    @staticmethod
    def get_available_months(year):

        connection = Database.get_connection()

        months = ExpenseRepository.get_available_months(
            connection,
            year
        )

        return [
            {
                "value": month,
                "name": calendar.month_name[month]
            }
            for month in months
        ]

    @staticmethod
    def get_monthly_report(year: int, month: int):

        total_expense = ExpenseRepository.get_total_expense(
            year,
            month
        )

        highest_category = ExpenseRepository.get_highest_expense_category(
            year,
            month
        )

        highest_transaction = ExpenseRepository.get_highest_transaction(
            year,
            month
        )

        category_summary = ExpenseRepository.get_category_aggregation(
            year,
            month
        )

        daily_trend = ExpenseRepository.get_daily_expense_trend(
            year,
            month
        )

        transactions = ExpenseRepository.get_transaction_summary(
            year,
            month
        )

        years = ExpenseRepository.get_available_years()

        months = [
            {
                "value": m,
                "name": calendar.month_name[m]
            }
            for m in ExpenseRepository.get_available_months(year)
        ]

        return {

        "years": years,
        "months": months,

        "selected_year": year,
        "selected_month": month,

        "total_expense": total_expense,

        "highest_category":
            highest_category["highest_category"],

        "highest_category_total":
            highest_category["highest_category_total"],

        "highest_transaction_store":
            highest_transaction["highest_transaction_store"],

        "highest_transaction_amount":
            highest_transaction["highest_transaction_amount"],

        "category_summary": category_summary,

        "daily_trend": daily_trend,

        "transactions": transactions,

    }


    @staticmethod
    def get_items_by_category(category_id: int):
        """
        Retrieve previously purchased items for a given expense category.

        Parameters
        ----------
        category_id : int
            Expense category ID.

        Returns
        -------
        list
            List of previous items within the category.
        """

        if not category_id:
            return []

        return ExpenseRepository.get_items_by_category(category_id)


    # ======================================================
    # Get Available Items
    # ======================================================
    @staticmethod
    def get_available_items(
        category_id=None,
        store_id=None,
        keyword=None
    ):

        return ExpenseRepository.get_available_items(
            category_id=category_id,
            store_id=store_id,
            keyword=keyword
        )