from loguru import logger
from sys import stdout

logger.remove()
logger.add(
    stdout,
    level="DEBUG",
    format="{time:YYYY-MM-DD at HH:mm:ss} | <level>{level}</level> | {message} | {extra}",
)

__all__ = ["logger"]
