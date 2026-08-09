# category_models.py

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Category:
    """
    Expense category master data.
    """

    category_id: Optional[int] = None
    category_name: str = ""
    is_active: Optional[int] = None