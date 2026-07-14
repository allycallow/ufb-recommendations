from os import getenv

import sentry_sdk
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

# --- OpenTelemetry Imports ---
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_fastapi_instrumentator import Instrumentator

from app.routers import (
    artist_router,
    label_router,
    playlist_router,
    release_router,
    track_router,
    user_router,
)

# ------------------------------


SENTRY_DSN = getenv("SENTRY_DSN", None)
STAGE = getenv("STAGE", "local")

sentry_sdk.init(dsn=SENTRY_DSN, send_default_pii=True, environment=STAGE)

app = FastAPI()


# --- OpenTelemetry Initialization ---
def initialize_tracing(fastapi_app: FastAPI):
    try:
        # Service name as it will appear inside the Jaeger UI dropdown
        resource = Resource.create(
            attributes={"service.name": "recommendations-service"}
        )
        provider = TracerProvider(resource=resource)

        # Reads target Jaeger gRPC endpoint from environment variables (e.g., OTEL_EXPORTER_OTLP_ENDPOINT)
        processor = BatchSpanProcessor(OTLPSpanExporter())
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)

        # Instrument FastAPI (extracts trace context from inbound Django headers automatically)
        FastAPIInstrumentor.instrument_app(
            fastapi_app, excluded_urls="metrics,sentry-debug"
        )
        print("OpenTelemetry tracing successfully initialized for FastAPI.")
    except Exception as e:
        print(f"Failed to initialize OpenTelemetry tracing: {e}")


# Trigger tracer registration immediately after FastAPI initialization
initialize_tracing(app)
# ------------------------------------


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "statusCode": exc.status_code,
        },
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sentry-debug")
async def trigger_error():
    raise Exception("This is a test exception for Sentry debugging")


# Application Routers
app.include_router(label_router, prefix="/labels", tags=["labels"])
app.include_router(artist_router, prefix="/artists", tags=["artists"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(release_router, prefix="/releases", tags=["releases"])
app.include_router(track_router, prefix="/tracks", tags=["tracks"])
app.include_router(playlist_router, prefix="/playlists", tags=["playlists"])

# Prometheus Metrics Exposer (Runs cleanly alongside OTel Tracing)
Instrumentator().instrument(app, metric_namespace="ufb_recommendations").expose(app)
