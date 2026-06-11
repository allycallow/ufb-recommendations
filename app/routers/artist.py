from fastapi import APIRouter, Depends

import app.db as db
from app.auth import verify_api_key
from app.schemas import StringListResponse
from app.utils import logger

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get(
    "/{artist_id}/related-artists",
    description="Get related artists for an artist",
    tags=["artists"],
    response_model=StringListResponse,
)
async def get_artist_related_artists(artist_id: str):
    logger.info(f"Getting related artists for artist {artist_id}")
    items = db.get_artist_related_artists(artist_id)
    return {
        "success": True,
        "items": list(map(lambda x: x["id"], items)),
    }


@router.get(
    "/trending",
    description="Get trending artists",
    tags=["artists"],
    response_model=StringListResponse,
)
async def get_trending_artists():
    logger.info("Getting trending tracks")
    items = db.get_trending_artists()
    return {
        "success": True,
        "items": items,
    }
