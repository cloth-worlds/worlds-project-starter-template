"""API routes for My Project Name."""

from fastapi import APIRouter

from my_app.core.logger import get_logger

log = get_logger(__name__)

# TODO: Update prefix and tags for your project
router = APIRouter(prefix="/my-app", tags=["my-app"])


@router.get("/status")
async def status():
    """Service status endpoint."""
    return {"service": "my-app", "status": "ok"}
