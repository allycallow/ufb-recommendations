from fastapi import APIRouter, Depends

from app.auth import verify_api_key
from app.utils import logger

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get(
    "/{user_id}/explore",
    description="Get explore recommendations for a user",
    tags=["users"],
)
async def get_user_explore(user_id: int):
    logger.info(f"Getting explore recommendations for user {user_id}")
    return {
        "success": True,
    }


@router.get(
    "/{user_id}/recommendations",
    description="Get recommendations for a user",
    tags=["users"],
)
async def get_user_recommendations(user_id: int):
    logger.info(f"Getting recommendations for user {user_id}")
    return {
        "success": True,
    }


@router.get(
    "/{user_id}/more-like-release",
    description="Get more like this release recommendations for a user",
    tags=["users"],
)
async def get_user_more_like_release(user_id: int):
    logger.info(f"Getting more like this release recommendations for user {user_id}")
    return {
        "success": True,
    }


@router.get(
    "/{user_id}/more-like-artist",
    description="Get more like this artist recommendations for a user",
    tags=["users"],
)
async def get_user_more_like_artist(user_id: int):
    logger.info(f"Getting more like this artist recommendations for user {user_id}")
    return {
        "success": True,
    }
