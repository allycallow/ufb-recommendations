from fastapi import APIRouter, Depends

import app.db as db
from app.auth import verify_api_key
from app.schemas import StringListResponse
from app.utils import logger

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get(
    "/{playlist_id}/suggested-tracks",
    description="Get suggested tracks for a playlist",
    tags=["playlists"],
    response_model=StringListResponse,
)
async def get_playlist_suggested_tracks(playlist_id: str):
    logger.info(f"Getting suggested tracks for playlist {playlist_id}")
    items = db.get_playlist_suggested_tracks(playlist_id)
    return {
        "success": True,
        "items": items,
    }
