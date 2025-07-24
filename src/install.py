import json
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import gzip


from db.db import init_db
from lib.logger import logger
from settings import settings


def _backup_db(minimize: bool = False, gz: bool = True):
    backup_data: dict = {}
    backup_file = Path(
        settings.DATA_DIR
        / f"{datetime.now(ZoneInfo('UTC')).strftime('%Y-%m-%d_%H-%M-%SZ')}-backup_data.json"
    )
    if gz:
        backup_file = backup_file.with_suffix(".json.gz")
    logger.info("Backing up database...")
    from db.db import MealRepository, SideDishRepository

    meal_repo = MealRepository()
    side_dish_repo = SideDishRepository()
    backup_data["meals"] = [
        meal.model_dump(mode="json") for meal in meal_repo.get_all_meals()
    ]
    backup_data["side_dishes"] = [
        side_dish.model_dump(mode="json")
        for side_dish in side_dish_repo.get_all_side_dishes()
    ]

    with gzip.open(backup_file, "wb") if gz else open(backup_file, "w") as f:
        f.write(
            json.dumps(
                backup_data, indent=2 if not minimize else None, ensure_ascii=False
            ).encode("utf-8")
        )


def install():
    _backup_db()
    logger.info("Installing database...")
    init_db()


if __name__ == "__main__":
    install()
