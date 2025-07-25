"""Backup and restore endpoints for the meal planner application."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(prefix="/api/backup", tags=["backup"])


@router.get("/export")
def export_data() -> FileResponse:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/import")
def import_data() -> FileResponse:
    raise HTTPException(status_code=501, detail="Not implemented")
