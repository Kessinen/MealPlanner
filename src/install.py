from db.db import init_db
from lib.logger import logger


def install():
    logger.info("Installing database...")
    init_db()


if __name__ == "__main__":
    install()
