"""Backup and restore utilities for the meal planner application."""

import gzip
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from db.repositories.meal import MealRepository
from db.repositories.side_dish import SideDishRepository
from db.repositories.meal_history import MealHistoryRepository
from lib.logger import logger
from settings import settings


def _write_backup_file(
    backup_file: Path, backup_data: dict, minimize: bool = False, gz: bool = True
) -> None:
    try:
        with gzip.open(backup_file, "wb") if gz else open(backup_file, "w") as f:
            content = json.dumps(
                backup_data,
                indent=2 if not minimize else None,
                ensure_ascii=False,
                default=str,
            )
            if gz:
                f.write(content.encode("utf-8"))
            else:
                f.write(content)

        logger.info(f"Backup created successfully: {backup_file}")
        return backup_file

    except Exception as e:
        logger.error(f"Error creating backup: {e}")
        raise


def create_backup(minimize: bool = False, gz: bool = True) -> Path:
    """Create a backup of the current database state.

    Args:
        minimize: Whether to minimize the JSON output (no indentation).
        gz: Whether to compress the backup with gzip.

    Returns:
        Path: The path to the created backup file.
    """
    backup_data: dict = {}

    # Generate backup filename with timestamp
    backup_file = Path(
        settings.DATA_DIR
        / f"{datetime.now(ZoneInfo('UTC')).strftime('%Y-%m-%d_%H-%M-%SZ')}-backup_data.json"
    )

    if gz:
        backup_file = backup_file.with_suffix(".json.gz")

    logger.info("Creating database backup...")

    # Get current data using repositories
    meal_repo = MealRepository()
    side_dish_repo = SideDishRepository()
    meal_history_repo = MealHistoryRepository()

    # Serialize models to dictionaries
    meals = meal_repo.get_all_meals()
    logger.debug(f"Fetched {len(meals) if meals else 0} meals from database")
    if meals:
        backup_data["meals"] = [meal.model_dump(mode="json") for meal in meals]

    side_dishes = side_dish_repo.get_all_side_dishes()
    logger.debug(
        f"Fetched {len(side_dishes) if side_dishes else 0} side dishes from database"
    )
    if side_dishes:
        backup_data["side_dishes"] = [
            side_dish.model_dump(mode="json") for side_dish in side_dishes
        ]

    meal_history = meal_history_repo.get_all_meal_history()
    logger.debug(
        f"Fetched {len(meal_history.history) if meal_history else 0} meal history items from database"
    )
    if meal_history:
        backup_data["meal_history"] = [
            meal_history_item.model_dump(mode="json")
            for meal_history_item in meal_history.history
        ]

    logger.debug(f"Backup data: {backup_data}")

    # Write backup file
    _write_backup_file(backup_file, backup_data, minimize, gz)

    logger.info(f"Backup created successfully: {backup_file}")

    # TODO: Implement message model here.


def truncate_all_tables():
    """Truncate all data from meals, side_dishes, and meal_history tables."""
    logger.info("Truncating all tables...")

    from db.core.connection import get_connection

    try:
        with get_connection() as conn:
            # Disable foreign key constraints temporarily
            conn.execute("SET session_replication_role = 'replica';")

            # Truncate tables in dependency order (reverse of import order)
            conn.execute("TRUNCATE TABLE meal_history RESTART IDENTITY CASCADE;")
            conn.execute("TRUNCATE TABLE meals RESTART IDENTITY CASCADE;")
            conn.execute("TRUNCATE TABLE side_dishes RESTART IDENTITY CASCADE;")

            # Re-enable foreign key constraints
            conn.execute("SET session_replication_role = 'origin';")

            logger.info("All tables truncated successfully")

    except Exception as e:
        logger.error(f"Error truncating tables: {e}")
        raise


def backup_and_truncate() -> Path:
    """Create a backup and then truncate all tables.

    Returns:
        Path: The path to the created backup file.
    """
    backup_path = create_backup()
    truncate_all_tables()
    return backup_path
