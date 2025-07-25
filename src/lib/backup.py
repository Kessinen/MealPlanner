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
    backup_data["meals"] = []
    meals = meal_repo.get_all_meals()
    if meals:
        backup_data["meals"] = [meal.model_dump(mode="json") for meal in meals]
    
    backup_data["side_dishes"] = []
    side_dishes = side_dish_repo.get_all_side_dishes()
    if side_dishes:
        backup_data["side_dishes"] = [side_dish.model_dump(mode="json") for side_dish in side_dishes]
    
    backup_data["meal_history"] = []
    meal_history = meal_history_repo.get_all_meal_history()
    if meal_history and meal_history.history:
        backup_data["meal_history"] = [
            {
                "id": str(idx),  # Generate unique ID
                "meal_id": item.meal.id if hasattr(item.meal, 'id') else str(item.meal),
                "date": item.date_eaten.isoformat() if hasattr(item.date_eaten, 'isoformat') else str(item.date_eaten),
                "side_dish": item.side_dish if item.side_dish else None,
                "created_at": datetime.now(ZoneInfo('UTC')).isoformat(),
                "updated_at": datetime.now(ZoneInfo('UTC')).isoformat(),
            }
            for idx, item in enumerate(meal_history.history)
        ]
    
    # Write backup file
    try:
        with gzip.open(backup_file, "wb") if gz else open(backup_file, "w") as f:
            content = json.dumps(
                backup_data, 
                indent=2 if not minimize else None, 
                ensure_ascii=False,
                default=str
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
