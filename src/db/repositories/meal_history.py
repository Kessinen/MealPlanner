"""Repository for meal history-related database operations."""

from fastapi import HTTPException

from models.meals import MealHistory, MealHistoryItem
from ..core.connection import get_connection
from .meal import MealRepository
from .side_dish import SideDishRepository
from lib import logger


class MealHistoryRepository:
    """Repository class for handling MealHistory database operations."""

    def __init__(self):
        logger.debug("Initializing MealHistoryRepository")
        self._connection = get_connection
        self._meal_repo = MealRepository()
        self._side_dish_repo = SideDishRepository()

    def get_all_meal_history(self) -> MealHistory | None:
        """Retrieve all meal history records from the database.

        Returns:
            MealHistory | None: MealHistory object containing history items if successful, None otherwise.
        """
        logger.debug("Fetching all meal history from database")

        try:
            with self._connection() as conn:
                logger.debug("Connected to database, executing query")

                # Get all history items using the meal_history_view
                query = """
                    SELECT 
                        date_eaten,
                        meal,
                        side_dish
                    FROM meal_history_view
                    ORDER BY date_eaten DESC, id
                """
                logger.debug("Executing SQL query")
                conn.execute(query)

                rows = conn.fetchall()
                logger.debug(f"Fetched {len(rows)} rows from database")

                if not rows:
                    logger.info("No meal history records found in database")
                    return MealHistory(history=[])

                # Log first few rows for debugging
                sample_size = min(3, len(rows))
                logger.debug(f"Sample of fetched rows: {rows[:sample_size]}")

                # Convert rows to MealHistoryItem objects
                history_items = []
                for row in rows:
                    try:
                        item = MealHistoryItem(
                            date_eaten=row["date_eaten"],
                            meal=row["meal"],
                            side_dish=row["side_dish"],
                        )
                        history_items.append(item)
                    except Exception as item_error:
                        logger.error(
                            f"Error creating MealHistoryItem from row {row}: {item_error}",
                            exc_info=True,
                        )
                        raise

                logger.debug(f"Created {len(history_items)} MealHistoryItem objects")

                try:
                    result = MealHistory(history=history_items)
                    logger.debug("Successfully created MealHistory object")
                    return result
                except Exception as history_error:
                    logger.error(
                        f"Error creating MealHistory: {history_error}", exc_info=True
                    )
                    raise

        except Exception as e:
            logger.error(
                f"Unexpected error in get_all_meal_history: {e}", exc_info=True
            )
            return None

    def add_meal_history(self, meal_history: MealHistoryItem):
        """Add a new meal history item to the database.

        Args:
            meal_history: The meal history item to add, containing meal and side dish names.

        Raises:
            HTTPException: If the meal is not found or there's a database error.
        """
        try:
            # Look up meal by name if we don't have an ID
            if not hasattr(meal_history.meal, "id"):
                meal = self._meal_repo.get_meal_by_name(meal_history.meal)
                if not meal:
                    raise HTTPException(
                        status_code=404, detail=f"Meal not found: {meal_history.meal}"
                    )
                meal_id = meal.id
            else:
                meal_id = meal_history.meal.id

            # Look up side dish by name if provided and we don't have an ID
            side_dish_id = None
            if meal_history.side_dish:
                if not hasattr(meal_history.side_dish, "id"):
                    side_dish = self._side_dish_repo.get_side_dish_by_name(
                        meal_history.side_dish
                    )
                    if side_dish:
                        side_dish_id = side_dish.id
                else:
                    side_dish_id = meal_history.side_dish.id

            with self._connection() as conn:
                conn.execute(
                    """
                    INSERT INTO meal_history (date_eaten, meal_id, side_dish_id)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        meal_history.date_eaten,
                        meal_id,
                        side_dish_id,
                    ),
                )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error adding meal history: {e}")
            raise HTTPException(
                status_code=500, detail=f"Failed to add meal history: {str(e)}"
            )
