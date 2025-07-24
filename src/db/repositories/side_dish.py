"""Repository for side dish-related database operations."""

from typing import Optional, List

from models.meals import SideDish
from ..core.connection import get_connection
from lib import logger


class SideDishRepository:
    """Repository class for handling SideDish database operations."""

    def __init__(self):
        self._connection = get_connection

    def get_all_side_dishes(self) -> Optional[List[SideDish]]:
        """Retrieve all side dishes from the database.

        Returns:
            Optional[List[SideDish]]: List of SideDish objects if successful, None otherwise.
        """
        try:
            with self._connection() as conn:
                conn.execute("""
                    SELECT id, name, notes, created_at, updated_at
                    FROM side_dishes
                    ORDER BY name
                """)
                rows = conn.fetchall()
                return [SideDish(**row) for row in rows] if rows else None
        except Exception as e:
            logger.error(f"Error fetching all side dishes: {e}")
            return None
