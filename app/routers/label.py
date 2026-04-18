import app.db as db
from fastapi import APIRouter, Depends

from app.auth import verify_api_key
from app.utils import logger

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get(
    "/{label_id}/related-artists",
    description="Get related artists for a label",
    tags=["labels"],
)
async def get_label_related_artists(label_id: str):
    logger.info(f"Getting related artists for label {label_id}")
    related_artists = db.get_label_related_artists(label_id)
    items = related_artists[0]["items"]
    return {
        "success": True,
        "items": list(map(lambda x: x["id"], items)),
    }
