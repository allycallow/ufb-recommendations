from fastapi import APIRouter, Depends

import app.db as db
from app.auth import verify_api_key
from app.utils import logger

router = APIRouter(dependencies=[Depends(verify_api_key)])


def format_recommendation(recommendations):
    def format_item(item):
        print(item)
        SK = item.get("SK", "")
        # Replace '#' with ':', lowercase, capitalize first letter
        id_val = SK.replace("#", ":").lower().capitalize()
        recommendation = {k: v for k, v in item.items() if k not in ("SK", "PK")}
        return {"id": id_val, **recommendation}

    formatted = [format_item(item) for item in recommendations]
    formatted.sort(key=lambda x: x.get("is_hero", 0), reverse=True)
    return formatted


@router.get(
    "/{user_id}/explore",
    description="Get explore recommendations for a user",
    tags=["users"],
)
async def get_user_explore(user_id: str):
    logger.info(f"Getting explore recommendations for user {user_id}")
    recommendations = db.get_explore(user_id)

    if len(recommendations) == 0:
        return {
            "success": True,
            "items": [],
        }

    return {
        "success": True,
        "items": format_recommendation(recommendations),
    }


@router.get(
    "/{user_id}/recommendations",
    description="Get recommendations for a user",
    tags=["users"],
)
async def get_user_recommendations(user_id: str):
    logger.info(f"Getting recommendations for user {user_id}")
    recommendations = db.get_recommendations(user_id)
    if len(recommendations) == 0:
        return {
            "success": True,
            "items": [],
        }
    return {
        "success": True,
        "items": format_recommendation(recommendations),
    }


@router.get(
    "/{user_id}/more-like-release",
    description="Get more like this release recommendations for a user",
    tags=["users"],
)
async def get_user_more_like_release(user_id: str):
    logger.info(f"Getting more like this release recommendations for user {user_id}")
    recommendations = db.get_more_like_release(user_id)
    if len(recommendations) == 0:
        return {
            "success": True,
            "items": [],
        }
    items = recommendations[0]["items"]
    return {
        "success": True,
        "items": items,
    }


@router.get(
    "/{user_id}/more-like-artist",
    description="Get more like this artist recommendations for a user",
    tags=["users"],
)
async def get_user_more_like_artist(user_id: str):
    logger.info(f"Getting more like this artist recommendations for user {user_id}")
    recommendations = db.get_more_like_artist(user_id)
    if len(recommendations) == 0:
        return {
            "success": True,
            "items": [],
        }
    items = recommendations[0]["items"]
    return {
        "success": True,
        "items": items,
    }
