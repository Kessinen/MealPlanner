"""Repository for meal-related database operations."""

from models.meals import Meal
from ..core.connection import get_connection
from lib import logger


class MealRepository:
    """Repository class for handling Meal database operations."""

    def __init__(self):
        self._connection = get_connection

    def get_all_meals(self) -> list[Meal] | None:
        """Retrieve all meals from the database.

        Returns:
            list[Meal] | None: List of Meal objects if successful, None otherwise.
        """
        try:
            with self._connection() as conn:
                conn.execute("""
                    SELECT 
                        id, name, 
                        string_to_array(trim(both '{}' from meal_types::text), ',') as meal_types,
                        notes, frequency_factor, active_time, passive_time, 
                        has_side_dish, created_at, updated_at
                    FROM meals
                    ORDER BY name
                """)
                rows = conn.fetchall()
                return [Meal(**row) for row in rows] if rows else None
        except Exception as e:
            logger.error(f"Error fetching all meals: {e}")
            return None

    def get_meal_by_id(self, meal_id: int) -> Meal | None:
        """Retrieve a single meal by its ID.

        Args:
            meal_id: The ID of the meal to retrieve.

        Returns:
            Meal | None: The Meal object if found, None otherwise.
        """
        try:
            with self._connection() as conn:
                conn.execute(
                    """
                    SELECT 
                        id, name, 
                        string_to_array(trim(both '{}' from meal_types::text), ',') as meal_types,
                        notes, frequency_factor, active_time, passive_time, 
                        has_side_dish, created_at, updated_at
                    FROM meals 
                    WHERE id = %s
                    """,
                    (meal_id,),
                )
                row = conn.fetchone()
                return Meal(**row) if row else None
        except Exception as e:
            logger.error(f"Error fetching meal with ID {meal_id}: {e}")
            return None

    def get_meal_by_name(self, meal_name: str) -> Meal | None:
        """Retrieve a single meal by its name.

        Args:
            meal_name: The name of the meal to retrieve.

        Returns:
            Meal | None: The Meal object if found, None otherwise.
        """
        try:
            with self._connection() as conn:
                conn.execute(
                    """
                    SELECT 
                        id, name, 
                        string_to_array(trim(both '{}' from meal_types::text), ',') as meal_types,
                        notes, frequency_factor, active_time, passive_time, 
                        has_side_dish, created_at, updated_at
                    FROM meals 
                    WHERE name = %s
                    """,
                    (meal_name,),
                )
                row = conn.fetchone()
                return Meal(**row) if row else None
        except Exception as e:
            logger.error(f"Error fetching meal with name {meal_name}: {e}")
            return None
