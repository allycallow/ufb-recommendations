import grpc

from app.auth import API_KEY
from app.utils import logger


class ApiKeyInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        metadata = dict(handler_call_details.invocation_metadata)
        api_key = metadata.get("x-api-key")

        if not api_key or api_key != API_KEY:
            logger.warning(
                f"gRPC request to {handler_call_details.method} rejected: "
                "missing or invalid API key"
            )

            async def deny(request, context):
                await context.abort(
                    grpc.StatusCode.UNAUTHENTICATED, "Missing or invalid API key"
                )

            return grpc.unary_unary_rpc_method_handler(deny)

        return await continuation(handler_call_details)
