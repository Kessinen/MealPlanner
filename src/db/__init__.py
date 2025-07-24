"""Database package for the Meal Planner application.

This package provides database connectivity and repository classes
for interacting with the application's database.

For database initialization and setup, see the `db.setup` module.
"""
from .core.connection import get_connection, test_connection
from .repositories import (
    MealRepository,
    SideDishRepository,
    MealHistoryRepository,
)
from .setup import initialize_database, seed_database

__all__ = [
    'get_connection',
    'test_connection',
    'MealRepository',
    'SideDishRepository',
    'MealHistoryRepository',
    'initialize_database',
    'seed_database',
]
