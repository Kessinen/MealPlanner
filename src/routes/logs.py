from fastapi import APIRouter, HTTPException
from pathlib import Path
from typing import Any
from enum import Enum

from models.logs import LogEntry
from settings import settings
from lib import logger

log_router = APIRouter(prefix="/logs", tags=["Logs"])


class LogLevel(Enum):
    ALL = "ALL"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def read_logs() -> list[dict[str, Any]]:
    """Read and parse log file into a list of log entries."""
    log_file = Path(settings.LOG_DIR) / "app.log"
    if not log_file.exists():
        return []

    logs = []
    with open(log_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                log_entry = LogEntry.model_validate_json(line)
                logs.append(log_entry.model_dump())
            except Exception as e:
                logger.warning(f"Failed to parse log line: {e}")
    return logs


@log_router.get("/")
async def get_logs():
    """Get all logs grouped by level."""
    try:
        entries = read_logs()
        return {
            "levels": {
                level.lower(): [
                    e for e in entries if e["record"]["level"]["name"] == level
                ]
                for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            }
        }
    except Exception as e:
        logger.error(f"Error reading logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to read logs")


@log_router.get("/{level}", response_model=list[LogEntry])
async def get_logs_by_level(level: LogLevel):
    """Get logs for a specific level (debug, info, warning, error, critical)."""
    level = level.value
    if level not in ["ALL", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise HTTPException(status_code=400, detail="Invalid log level")

    try:
        entries = read_logs()
        if level == "ALL":
            return entries
        return {level: [e for e in entries if e["record"]["level"]["name"] == level]}
    except Exception as e:
        logger.error(f"Error reading {level} logs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to read {level} logs")
