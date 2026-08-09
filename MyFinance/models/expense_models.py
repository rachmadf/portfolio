"""
==========================================================
MyFinance

Expense Domain Models
==========================================================
"""

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


# ==========================================================
# MASTER DATA
# ==========================================================

@dataclass(slots=True)
class Store:
    """
    Expense store / merchant.
    """

    store_id: Optional[int] = None
    store_name: str = ""
    created_at: Optional[str] = None


@dataclass(slots=True)
class PaymentMethod:
    """
    Payment method.
    """

    payment_method_id: Optional[int] = None
    payment_method_name: str = ""
    created_at: Optional[str] = None


@dataclass(slots=True)
class ExpenseCategory:
    """
    Expense category.
    """

    category_id: Optional[int] = None
    category_name: str = ""
    created_at: Optional[str] = None


# ==========================================================
# DETAIL
# ==========================================================

@dataclass(slots=True)
class ExpenseDetail:
    """
    One purchased item.
    """

    detail_id: Optional[int] = None
    transaction_id: Optional[int] = None
    category_id: int = 0
    item_name: str = ""
    # brand: str = ""
    size: str = ""
    quantity: float = 0.0
    unit_price: float = 0.0
    subtotal: float = 0.0
    created_at: Optional[str] = None

    def calculate_subtotal(self) -> float:
        """
        Calculate subtotal.
        """

        self.subtotal = round(
            self.quantity * self.unit_price,
            2
        )

        return self.subtotal


# ==========================================================
# HEADER
# ==========================================================

@dataclass(slots=True)
class ExpenseTransaction:
    """
    Expense transaction header.
    """

    transaction_id: Optional[int] = None
    expense_date: Optional[date] = None
    receipt_number: str = ""
    store_id: int = 0
    payment_method_id: int = 0
    notes: str = ""
    discount: float = 0.0
    grand_total: float = 0.0
    created_at: Optional[str] = None

    details: List[ExpenseDetail] = field(default_factory=list)

    def add_detail(
        self,
        detail: ExpenseDetail
    ) -> None:

        detail.calculate_subtotal()

        self.details.append(detail)

        self.calculate_total()

    def remove_detail(
        self,
        index: int
    ) -> None:

        self.details.pop(index)

        self.calculate_total()

    def calculate_subtotal(self) -> float:

        return round(

            sum(
                detail.calculate_subtotal()
                for detail in self.details
            ),

            2

        )

    def calculate_total(self) -> float:

        subtotal = self.calculate_subtotal()

        self.grand_total = round(

            subtotal - self.discount,

            2

        )

        if self.grand_total < 0:

            self.grand_total = 0.0

        return self.grand_total

    @property
    def total_items(self) -> int:

        return len(self.details)

    @property
    def total_quantity(self) -> float:

        return round(

            sum(
                detail.quantity
                for detail in self.details
            ),

            2

        )


# ==========================================================
# RESULT
# ==========================================================

@dataclass(slots=True)
class SaveExpenseResult:
    """
    Returned by Service after saving.
    """

    success: bool

    transaction_id: Optional[int] = None

    message: str = ""