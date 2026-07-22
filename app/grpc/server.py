from os import getenv

import grpc
from google.protobuf.struct_pb2 import Struct
from grpc_reflection.v1alpha import reflection

import app.db as db
from app.grpc import recommendations_pb2, recommendations_pb2_grpc
from app.grpc.interceptors import ApiKeyInterceptor
from app.routers.user import format_recommendation
from app.utils import logger

GRPC_PORT = getenv("GRPC_PORT", "50051")


def _to_structs(items: list[dict]) -> list[Struct]:
    structs = []
    for item in items:
        struct = Struct()
        struct.update(item)
        structs.append(struct)
    return structs


def _paginate(items: list[str], page: int, page_size: int) -> tuple[list[str], int]:
    page = page or 1
    page_size = page_size or 20
    total = len(items)
    start = (page - 1) * page_size
    return items[start : start + page_size], total


class RecommendationsServicer(recommendations_pb2_grpc.RecommendationsServiceServicer):
    async def GetArtistRelatedArtists(self, request, context):
        logger.info(f"gRPC getting related artists for artist {request.id}")
        items = db.get_artist_related_artists(request.id)
        return recommendations_pb2.StringListResponse(
            success=True, items=[item["id"] for item in items]
        )

    async def GetTrendingArtists(self, request, context):
        logger.info("gRPC getting trending artists")
        items = db.get_trending_artists()
        return recommendations_pb2.StringListResponse(success=True, items=items)

    async def GetArtistTopPicks(self, request, context):
        logger.info(f"gRPC getting top picks for artist {request.id}")
        all_items = db.get_artist_top_picks(request.id)
        items, total = _paginate(all_items, request.page, request.page_size)
        return recommendations_pb2.PaginatedStringListResponse(
            success=True,
            items=items,
            page=request.page or 1,
            page_size=request.page_size or 20,
            total=total,
        )

    async def GetLabelRelatedArtists(self, request, context):
        logger.info(f"gRPC getting related artists for label {request.id}")
        items = db.get_label_related_artists(request.id)
        return recommendations_pb2.StringListResponse(
            success=True, items=[item["id"] for item in items]
        )

    async def GetLabelTopPicks(self, request, context):
        logger.info(f"gRPC getting top picks for label {request.id}")
        all_items = db.get_label_top_picks(request.id)
        items, total = _paginate(all_items, request.page, request.page_size)
        return recommendations_pb2.PaginatedStringListResponse(
            success=True,
            items=items,
            page=request.page or 1,
            page_size=request.page_size or 20,
            total=total,
        )

    async def GetReleaseRecommendations(self, request, context):
        logger.info(f"gRPC getting recommendations for release {request.id}")
        recommendations = db.get_release_recommendations(request.id)
        if len(recommendations) == 0:
            return recommendations_pb2.StringListResponse(success=True, items=[])
        items = recommendations[0]["items"]["SS"]
        return recommendations_pb2.StringListResponse(success=True, items=items)

    async def GetTrendingTracks(self, request, context):
        logger.info("gRPC getting trending tracks")
        items = db.get_trending_tracks()
        return recommendations_pb2.StringListResponse(success=True, items=items)

    async def GetPlaylistSuggestedTracks(self, request, context):
        logger.info(f"gRPC getting suggested tracks for playlist {request.id}")
        all_items = db.get_playlist_suggested_tracks(request.id)
        items, total = _paginate(all_items, request.page, request.page_size)
        return recommendations_pb2.PaginatedStringListResponse(
            success=True,
            items=items,
            page=request.page or 1,
            page_size=request.page_size or 20,
            total=total,
        )

    async def GetUserExplore(self, request, context):
        logger.info(f"gRPC getting explore recommendations for user {request.id}")
        recommendations = db.get_explore(request.id)
        if len(recommendations) == 0:
            return recommendations_pb2.StructListResponse(success=True, items=[])
        return recommendations_pb2.StructListResponse(
            success=True, items=_to_structs(format_recommendation(recommendations))
        )

    async def GetUserRecommendations(self, request, context):
        logger.info(f"gRPC getting recommendations for user {request.id}")
        recommendations = db.get_recommendations(request.id)
        if len(recommendations) == 0:
            return recommendations_pb2.StructListResponse(success=True, items=[])
        return recommendations_pb2.StructListResponse(
            success=True, items=_to_structs(format_recommendation(recommendations))
        )

    async def GetUserMoreLikeRelease(self, request, context):
        logger.info(
            f"gRPC getting more like this release recommendations for user {request.id}"
        )
        recommendations = db.get_more_like_release(request.id)
        if len(recommendations) == 0:
            return recommendations_pb2.StructListResponse(success=True, items=[])
        items = recommendations[0]["items"]
        return recommendations_pb2.StructListResponse(
            success=True, items=_to_structs(items)
        )

    async def GetUserMoreLikeArtist(self, request, context):
        logger.info(
            f"gRPC getting more like this artist recommendations for user {request.id}"
        )
        recommendations = db.get_more_like_artist(request.id)
        if len(recommendations) == 0:
            return recommendations_pb2.StructListResponse(success=True, items=[])
        items = recommendations[0]["items"]
        return recommendations_pb2.StructListResponse(
            success=True, items=_to_structs(items)
        )

    async def GetUserTopPicks(self, request, context):
        logger.info(f"gRPC getting top picks recommendations for user {request.id}")
        recommendations = db.get_top_picks(request.id)
        if len(recommendations) == 0:
            return recommendations_pb2.StructListResponse(success=True, items=[])
        items = recommendations[0]["items"]
        return recommendations_pb2.StructListResponse(
            success=True, items=_to_structs(items)
        )


async def create_grpc_server() -> grpc.aio.Server:
    server = grpc.aio.server(interceptors=[ApiKeyInterceptor()])
    recommendations_pb2_grpc.add_RecommendationsServiceServicer_to_server(
        RecommendationsServicer(), server
    )

    reflection.enable_server_reflection(
        (
            recommendations_pb2.DESCRIPTOR.services_by_name[
                "RecommendationsService"
            ].full_name,
            reflection.SERVICE_NAME,
        ),
        server,
    )

    server.add_insecure_port(f"[::]:{GRPC_PORT}")
    return server
