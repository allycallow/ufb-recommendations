from fastapi import APIRouter, Depends, Query

import app.db as db
from app.auth import verify_api_key
from app.schemas import PaginatedStringListResponse
from app.utils import logger

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get(
    "/{playlist_id}/suggested-tracks",
    description="Get suggested tracks for a playlist",
    tags=["playlists"],
    response_model=PaginatedStringListResponse,
)
async def get_playlist_suggested_tracks(
    playlist_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
):
    logger.info(f"Getting suggested tracks for playlist {playlist_id}")
    all_items = db.get_playlist_suggested_tracks(playlist_id)
    total = len(all_items)
    start = (page - 1) * page_size
    items = all_items[start : start + page_size]
    return {
        "success": True,
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
    }
