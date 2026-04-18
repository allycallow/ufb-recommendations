from fastapi import APIRouter, Depends

from app.auth import verify_api_key
from app.utils import logger

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get(
    "/{release_id}/recommendations",
    description="Get recommendations for a release",
    tags=["releases"],
)
async def get_release_recommendations(release_id: int):
    logger.info(f"Getting recommendations for release {release_id}")
    return {
        "success": True,
    }
