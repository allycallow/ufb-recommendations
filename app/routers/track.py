from fastapi import APIRouter, Depends

import app.db as db
from app.auth import verify_api_key
from app.schemas import StringListResponse
from app.utils import logger

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get(
    "/trending",
    description="Get trending tracks",
    tags=["tracks"],
    response_model=StringListResponse,
)
async def get_trending_tracks():
    logger.info("Getting trending tracks")
    tracks = db.get_trending_tracks()
    items = [track["id"] for track in tracks]
    return {
        "success": True,
        "items": items,
    }
