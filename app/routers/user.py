import random

from fastapi import APIRouter, Depends

import app.db as db
from app.auth import verify_api_key
from app.schemas import (
    HomeResponse,
    MoreLikeArtistResponse,
    MoreLikeReleaseResponse,
    RecommendationListResponse,
    TypedListResponse,
)
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


def build_home_sections(user_id: str):
    sections = []

    more_like_release = db.get_more_like_release(user_id)
    for entry in more_like_release:
        sections.append(
            {
                "id": entry["id"],
                "target_id": entry["target_id"],
                "type": entry["type"],
                "subtitle": "More Like",
                "items": entry["recommendations"],
            }
        )

    more_like_artist = db.get_more_like_artist(user_id)
    for entry in more_like_artist:
        sections.append(
            {
                "id": entry["id"],
                "target_id": entry["target_id"],
                "type": entry["type"],
                "subtitle": "More Like",
                "items": entry["recommendations"],
            }
        )

    random.shuffle(sections)
    return sections


@router.get(
    "/{user_id}/explore",
    description="Get explore recommendations for a user",
    tags=["users"],
    response_model=RecommendationListResponse,
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
    response_model=RecommendationListResponse,
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
    response_model=MoreLikeReleaseResponse,
)
async def get_user_more_like_release(user_id: str):
    logger.info(f"Getting more like this release recommendations for user {user_id}")
    recommendations = db.get_more_like_release(user_id)
    items = [
        {
            "id": entry["id"],
            "target_id": entry["target_id"],
            "recommendations": entry["recommendations"],
        }
        for entry in recommendations
    ]
    return {
        "success": True,
        "items": items,
    }


@router.get(
    "/{user_id}/more-like-artist",
    description="Get more like this artist recommendations for a user",
    tags=["users"],
    response_model=MoreLikeArtistResponse,
)
async def get_user_more_like_artist(user_id: str):
    logger.info(f"Getting more like this artist recommendations for user {user_id}")
    recommendations = db.get_more_like_artist(user_id)
    items = [
        {
            "id": entry["id"],
            "target_id": entry["target_id"],
            "recommendations": entry["recommendations"],
        }
        for entry in recommendations
    ]
    return {
        "success": True,
        "items": items,
    }


@router.get(
    "/{user_id}/home",
    description="Get home feed for a user, combining more-like-release and "
    "more-like-artist recommendations",
    tags=["users"],
    response_model=HomeResponse,
)
async def get_user_home(user_id: str):
    logger.info(f"Getting home feed for user {user_id}")
    return {
        "success": True,
        "items": build_home_sections(user_id),
    }


@router.get(
    "/{user_id}/top-picks",
    description="Get top picks recommendations for a user",
    tags=["users"],
    response_model=TypedListResponse,
)
async def get_user_top_picks(user_id: str):
    logger.info(f"Getting top picks recommendations for user {user_id}")
    recommendations = db.get_top_picks(user_id)
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
