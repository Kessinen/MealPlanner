import psycopg
from contextlib import contextmanager
from pathlib import Path
from psycopg.rows import dict_row

from settings import settings
from lib.logger import logger
from models.meals import Meal, SideDish, MealHistoryItem, MealHistory


@contextmanager
def get_connection():
    conn = None
    cur = None
    try:
        conn = psycopg.connect(settings.db_url)
        cur = conn.cursor(row_factory=dict_row)
        cur.execute("SELECT 1")
        yield cur
    except psycopg.Error as e:
        if conn:
            conn.rollback()
        logger.error(e)
    finally:
        conn.commit()
        if cur:
            cur.close()
        if conn:
            conn.close()


def test_connection():
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
    except psycopg.Error as e:
        logger.error(e)
        return False
    logger.debug("Database connection test successful")
    return True


def _seed_db():
    import json

    logger.info("Seeding database...")

    with open(Path(__file__).parent / "seed_meals.json", "r") as f:
        meals = json.load(f)
    with open(Path(__file__).parent / "seed_sidedishes.json", "r") as f:
        side_dishes = json.load(f)

    meals = sorted(meals, key=lambda x: x["name"])
    side_dishes = sorted(side_dishes, key=lambda x: x["name"])

    with get_connection() as conn:
        logger.debug("Seeding meals...")
        for meal in meals:
            try:
                # Convert meal_type list to PostgreSQL array format
                meal_types = "{" + ",".join(f'"{t}"' for t in meal["meal_types"]) + "}"
                conn.execute(
                    """
                    INSERT INTO meals 
                    (name, meal_types, notes, frequency_factor, active_time, passive_time, has_side_dish) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        meal["name"],
                        meal_types,  # This will be properly cast to meal_type[] by psycopg
                        meal["notes"],
                        meal["frequency_factor"],
                        meal["active_time"],
                        meal["passive_time"],
                        meal["has_side_dish"],
                    ),
                )
            except psycopg.Error as e:
                conn.connection.rollback()
                logger.error(e)
                return
        logger.debug("Seeding side dishes...")
        for side_dish in side_dishes:
            try:
                conn.execute(
                    """
                    INSERT INTO side_dishes 
                    (name, notes) 
                    VALUES (%s, %s)
                    """,
                    (side_dish["name"], side_dish["notes"]),
                )
            except psycopg.Error as e:
                conn.connection.rollback()
                logger.error(e)
                return


def init_db():
    logger.info("Initializing database...")

    # Get all SQL files and sort them by their numeric prefix
    sql_dir = Path(__file__).parent
    sql_files = []

    # First collect all SQL files with numeric prefixes
    for sql_file in sql_dir.glob("*.sql"):
        try:
            # Extract the numeric prefix
            prefix = int(sql_file.stem.split("_")[0])
            sql_files.append((prefix, sql_file))
        except (ValueError, IndexError):
            # Skip files that don't start with a number
            logger.warning(f"Skipping SQL file without numeric prefix: {sql_file}")

    # Sort by the numeric prefix
    sql_files.sort(key=lambda x: x[0])

    if not sql_files:
        logger.error("No valid SQL files found")
        return

    with get_connection() as conn:
        for _, sql_file in sql_files:
            logger.debug(f"Executing {sql_file}")
            try:
                conn.execute(open(sql_file).read())

                logger.debug(f"Successfully executed {sql_file.name}")
            except psycopg.Error as e:
                logger.error(f"Error executing {sql_file.name}: {str(e)}")
                # Don't stop on error, try to continue with other files
                logger.error("Database initialization failed")
                conn.connection.rollback()
                return

        conn.connection.commit()
    logger.info("Database initialization completed")
    _seed_db()


class MealRepository:
    def __init__(self):
        self._connection = get_connection

    def get_all_meals(self) -> list[Meal] | None:
        rows = None
        with self._connection() as conn:
            try:
                conn.execute("""
                    SELECT 
                        id, name, 
                        string_to_array(trim(both '{}' from meal_types::text), ',') as meal_types,
                        notes, frequency_factor, active_time, passive_time, has_side_dish, created_at, updated_at
                    FROM meals
                """)
            except psycopg.Error as e:
                logger.error(e)
                return None
            rows = conn.fetchall()
            if not rows:
                return None
        # Map meal_types to meal_type for the Pydantic model
        # for row in rows:
        # row["meal_type"] = row["meal_types"]
        return [Meal(**row) for row in rows]

    def get_meal_by_id(self, meal_id: int) -> Meal | None:
        with self._connection() as conn:
            try:
                conn.execute(
                    """
                    SELECT 
                        id, name, 
                        string_to_array(trim(both '{}' from meal_types::text), ',') as meal_types,
                        notes, frequency_factor, active_time, passive_time, has_side_dish, created_at, updated_at
                    FROM meals 
                    WHERE id = %s
                """,
                    (meal_id,),
                )
            except psycopg.Error as e:
                logger.error(e)
                return None
            return Meal(**conn.fetchone())


class SideDishRepository:
    def __init__(self):
        self._connection = get_connection

    def get_all_side_dishes(self) -> list[SideDish] | None:
        rows = None
        with self._connection() as conn:
            try:
                conn.execute("""
                    SELECT 
                        id, name, notes, created_at, updated_at
                    FROM side_dishes
                """)
            except psycopg.Error as e:
                logger.error(e)
                return None
            rows = conn.fetchall()
            if not rows:
                return None
        return [SideDish(**row) for row in rows]


class MealHistoryRepository:
    def __init__(self):
        self._connection = get_connection

    def get_all_meal_history(self) -> list[MealHistoryItem] | None:
        rows = None
        with self._connection() as conn:
            try:
                conn.execute("""
                    SELECT 
                        id, date_eaten, meal, side_dish, created_at, updated_at
                    FROM meal_history
                """)
            except psycopg.Error as e:
                logger.error(e)
                return None
            rows = conn.fetchall()
            if not rows:
                return None
        return MealHistory(history=[MealHistoryItem(**row) for row in rows])
