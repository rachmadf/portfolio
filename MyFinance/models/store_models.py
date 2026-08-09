# store_models.py

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Store:
    """
    Store master data.
    """

    store_id: Optional[int] = None
    store_name: str = ""
    is_active: Optional[int] = None