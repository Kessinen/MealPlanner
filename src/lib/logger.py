from loguru import logger
from sys import stdout
from pathlib import Path

from settings import settings

logger.remove()
logger.add(
    stdout,
    level="DEBUG",
    format="{time:YYYY-MM-DD at HH:mm:ss} | <level>{level}</level> | {file}:{line} | {message} | {extra}",
)

logger.add(
    Path(settings.LOG_DIR) / "app.log",
    level="INFO",
    format="{level} | {file}:{line} | {message}",
    rotation="3 days",
    retention="1 month",
    compression="gz",
    encoding="utf-8",
    enqueue=True,
    serialize=True,
)

__all__ = ["logger"]
