from fastapi import APIRouter, Depends, Query

import app.db as db
from app.auth import verify_api_key
from app.schemas import PaginatedStringListResponse, StringListResponse
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


@router.get(
    "/{artist_id}/top-picks",
    description="Get top picks for an artist",
    tags=["artists"],
    response_model=PaginatedStringListResponse,
)
async def get_artist_top_picks(
    artist_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
):
    logger.info(f"Getting top picks for artist {artist_id}")
    all_items = db.get_artist_top_picks(artist_id)
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
