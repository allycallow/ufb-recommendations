from fastapi import APIRouter, Depends

import app.db as db
from app.auth import verify_api_key
from app.schemas import StringListResponse
from app.utils import logger

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get(
    "/{label_id}/related-artists",
    description="Get related artists for a label",
    tags=["labels"],
    response_model=StringListResponse,
)
async def get_label_related_artists(label_id: str):
    logger.info(f"Getting related artists for label {label_id}")
    items = db.get_label_related_artists(label_id)
    return {
        "success": True,
        "items": list(map(lambda x: x["id"], items)),
    }
