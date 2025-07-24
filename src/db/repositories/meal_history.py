"""Repository for meal history-related database operations."""

from models.meals import MealHistory, MealHistoryItem
from ..core.connection import get_connection
from lib import logger


class MealHistoryRepository:
    """Repository class for handling MealHistory database operations."""

    def __init__(self):
        logger.debug("Initializing MealHistoryRepository")
        self._connection = get_connection

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
