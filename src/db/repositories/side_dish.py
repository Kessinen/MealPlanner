"""Repository for side dish-related database operations."""

from models.meals import SideDish
from ..core.connection import get_connection
from lib import logger


class SideDishRepository:
    """Repository class for handling SideDish database operations."""

    def __init__(self):
        self._connection = get_connection

    def get_all_side_dishes(self) -> list[SideDish] | None:
        """Retrieve all side dishes from the database.

        Returns:
            list[SideDish] | None: List of SideDish objects if successful, None otherwise.
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

    def get_side_dish_by_name(self, side_dish_name: str) -> SideDish | None:
        """Retrieve a single side dish by its name.

        Args:
            side_dish_name: The name of the side dish to retrieve.

        Returns:
            SideDish | None: The SideDish object if found, None otherwise.
        """
        try:
            with self._connection() as conn:
                conn.execute(
                    """
                    SELECT 
                        id, name, notes, created_at, updated_at
                    FROM side_dishes 
                    WHERE name = %s
                    """,
                    (side_dish_name,),
                )
                row = conn.fetchone()
                return SideDish(**row) if row else None
        except Exception as e:
            logger.error(f"Error fetching side dish with name {side_dish_name}: {e}")
            return None
