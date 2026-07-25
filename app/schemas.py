from typing import Optional

from pydantic import BaseModel


class StringListResponse(BaseModel):
    success: bool
    items: list[str]


class RecommendationSubItem(BaseModel):
    model_config = {"extra": "allow"}

    id: str
    title: Optional[str] = None
    artwork: Optional[str] = None


class RecommendationMeta(BaseModel):
    types: list[str]
    next_update_date: str


class RecommendationItem(BaseModel):
    id: str
    title: str
    items: list[RecommendationSubItem]
    meta: RecommendationMeta
    is_hero: Optional[int] = None


class RecommendationListResponse(BaseModel):
    success: bool
    items: list[RecommendationItem]


class TypedItem(BaseModel):
    type: str
    id: str


class TypedListResponse(BaseModel):
    success: bool
    items: list[TypedItem]


class MoreLikeArtistItem(BaseModel):
    id: str
    target_id: str
    recommendations: list[str]


class MoreLikeArtistResponse(BaseModel):
    success: bool
    items: list[MoreLikeArtistItem]


class MoreLikeReleaseItem(BaseModel):
    id: str
    target_id: str
    recommendations: list[str]


class MoreLikeReleaseResponse(BaseModel):
    success: bool
    items: list[MoreLikeReleaseItem]


class PaginatedStringListResponse(BaseModel):
    success: bool
    items: list[str]
    page: int
    page_size: int
    total: int


class HomeSection(BaseModel):
    id: str
    target_id: str
    type: str
    title: Optional[str] = None
    subtitle: Optional[str] = None
    items: list[str]


class HomeResponse(BaseModel):
    success: bool
    items: list[HomeSection]
