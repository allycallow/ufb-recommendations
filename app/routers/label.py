from fastapi import APIRouter, Depends

from app.auth import verify_api_key
from app.utils import logger

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get(
    "/{label_id}/related-artists",
    description="Get related artists for a label",
    tags=["labels"],
)
async def get_label_related_artists(label_id: int):
    logger.info(f"Getting related artists for label {label_id}")
    return {
        "success": True,
    }
