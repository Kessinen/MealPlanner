import psycopg
from contextlib import contextmanager
from fastapi import HTTPException
from pathlib import Path

from settings import settings
from lib.logger import logger


@contextmanager
def get_connection():
    conn = None
    cur = None
    try:
        conn = psycopg.connect(settings.db_url)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        yield cur
    except psycopg.Error as e:
        if conn:
            conn.rollback()
        logger.critical(e)
    finally:
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
    pass


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

    errors: bool = False
    with get_connection() as conn:
        for _, sql_file in sql_files:
            logger.debug(f"Executing {sql_file}")
            try:
                conn.execute(open(sql_file).read())

                logger.debug(f"Successfully executed {sql_file.name}")
            except psycopg.Error as e:
                logger.error(f"Error executing {sql_file.name}: {str(e)}")
                # Don't stop on error, try to continue with other files
                errors = True
                break
        conn.connection.commit()
        if errors:
            logger.error("Database initialization failed")
        else:
            logger.info("Database initialization completed")


class MealRepository:
    def __init__(self):
        self._connection = get_connection()

    def get_all_meals(self):
        with self._connection() as conn:
            try:
                conn.execute("SELECT * FROM meals")
            except psycopg.Error as e:
                logger.error(e)
        return conn.fetchall()

    def get_meal_by_id(self, meal_id: int):
        with self._connection() as conn:
            try:
                conn.execute("SELECT * FROM meals WHERE id = %s", (meal_id,))
            except psycopg.Error as e:
                logger.error(e)
                raise HTTPException(status_code=500, detail=str(e))
        return conn.fetchone()
