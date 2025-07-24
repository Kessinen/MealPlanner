"""Repository for meal history-related database operations."""

from typing import Optional, List

from models.meals import MealHistory, MealHistoryItem
from ..core.connection import get_connection
from lib import logger


class MealHistoryRepository:
    """Repository class for handling MealHistory database operations."""

    def __init__(self):
        self._connection = get_connection

    def get_all_meal_history(self) -> Optional[List[MealHistory]]:
        """Retrieve all meal history records from the database.

        Returns:
            Optional[List[MealHistory]]: List of MealHistory objects if successful, None otherwise.
        """
        try:
            with self._connection() as conn:
                # First get all history entries
                conn.execute("""
                    SELECT id, date, notes, created_at, updated_at
                    FROM meal_history
                    ORDER BY date DESC
                """)
                history_entries = conn.fetchall()

                if not history_entries:
                    return None

                # For each history entry, get its items
                result = []
                for entry in history_entries:
                    conn.execute(
                        """
                        SELECT mhi.id, mhi.meal_id, m.name as meal_name, 
                               mhi.side_dish_id, sd.name as side_dish_name,
                               mhi.rating, mhi.notes
                        FROM meal_history_items mhi
                        LEFT JOIN meals m ON mhi.meal_id = m.id
                        LEFT JOIN side_dishes sd ON mhi.side_dish_id = sd.id
                        WHERE mhi.meal_history_id = %s
                    """,
                        (entry["id"],),
                    )

                    items = [MealHistoryItem(**row) for row in conn.fetchall()]
                    history = MealHistory(**entry, items=items)
                    result.append(history)

                return result

        except Exception as e:
            logger.error(f"Error fetching meal history: {e}")
            return None
