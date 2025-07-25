from db.setup import initialize_database, seed_database
from lib.backup import create_backup
from lib import logger


def _backup_db(minimize: bool = False, gz: bool = True):
    """Create a backup before installation."""
    backup_path = create_backup(minimize=minimize, gz=gz)
    logger.info(f"Database backed up to: {backup_path}")


def install():
    _backup_db()
    logger.info("Installing database...")
    if not initialize_database():
        logger.error("Database initialization failed")
        return
    if not seed_database():
        logger.error("Database seeding failed")
        return


if __name__ == "__main__":
    install()
