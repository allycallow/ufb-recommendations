import app.db as db
from fastapi import APIRouter, Depends
from app.auth import verify_api_key
from app.utils import logger


router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get(
    "/{artist_id}/related-artists",
    description="Get related artists for an artist",
    tags=["artists"],
)
async def get_artist_related_artists(artist_id: str):
    logger.info(f"Getting related artists for artist {artist_id}")
    related_artists = db.get_artist_related_artists(artist_id)
    items = related_artists[0]["items"]
    return {
        "success": True,
        "items": list(map(lambda x: x["id"], items)),
    }
