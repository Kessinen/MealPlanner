"""Repository implementations for database operations.

This package contains repository classes that handle database operations for different
domain models. Each repository is responsible for a specific domain entity and provides
methods to interact with its corresponding database tables.
"""

from .meal import MealRepository
from .side_dish import SideDishRepository
from .meal_history import MealHistoryRepository

__all__ = [
    "MealRepository",
    "SideDishRepository",
    "MealHistoryRepository",
]
