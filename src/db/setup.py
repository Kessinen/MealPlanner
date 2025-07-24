"""Database setup and initialization utilities.

This module contains functions for setting up and initializing the database,
including creating tables and seeding initial data. These functions are typically
only run during application installation or setup.
"""

import json
import logging
from pathlib import Path

from .core.connection import get_connection

logger = logging.getLogger(__name__)


def seed_database() -> None:
    """Seed the database with initial data.

    This function loads meal and side dish data from JSON files and inserts them
    into the database.
    """
    logger.info("Seeding database...")

    try:
        with open(Path(__file__).parent / "seeds/meals.json", "r") as f:
            meals = sorted(json.load(f), key=lambda x: x["name"])
        with open(Path(__file__).parent / "seeds/side_dishes.json", "r") as f:
            side_dishes = sorted(json.load(f), key=lambda x: x["name"])
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error loading seed files: {e}")
        return

    with get_connection() as conn:
        logger.debug("Seeding meals...")
        for meal in meals:
            # Convert meal_type list to PostgreSQL array format
            meal_types = "{" + ",".join(f'"{t}"' for t in meal["meal_types"]) + "}"
            try:
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
            except Exception as e:
                logger.error(f"Error seeding meal {meal.get('name')}: {e}")
                raise

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
            except Exception as e:
                logger.error(f"Error seeding side dish {side_dish.get('name')}: {e}")
                raise


def initialize_database() -> bool:
    """Initialize the database by running all SQL migration files in order.

    SQL files should be named with a numeric prefix (e.g., '001_initial_schema.sql').
    After running migrations, the database will be seeded with initial data.

    Returns:
        bool: True if initialization was successful, False otherwise.
    """
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
            continue

    # Sort by the numeric prefix
    sql_files.sort(key=lambda x: x[0])

    if not sql_files:
        logger.error("No valid SQL files found")
        return False

    try:
        with get_connection() as conn:
            for _, sql_file in sql_files:
                logger.debug(f"Executing {sql_file}")
                try:
                    conn.execute(open(sql_file).read())
                    logger.debug(f"Successfully executed {sql_file.name}")
                except Exception as e:
                    logger.error(f"Error executing {sql_file.name}: {e}")
                    return False

            # Only seed if all migrations were successful
            logger.info("Database initialization completed successfully")
            return True

    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {e}")
        return False
