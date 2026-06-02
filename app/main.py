from os import getenv

import sentry_sdk
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

# --- OpenTelemetry Imports ---
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# ------------------------------

from app.routers import artist_router, label_router, release_router, user_router

SENTRY_DSN = getenv("SENTRY_DSN", None)
STAGE = getenv("STAGE", "local")

sentry_sdk.init(dsn=SENTRY_DSN, send_default_pii=True, environment=STAGE)

app = FastAPI()


# --- OpenTelemetry Initialization ---
def initialize_tracing(fastapi_app: FastAPI):
    try:
        # Service name identifier for the Jaeger UI dropdown
        resource = Resource.create(
            attributes={"service.recommendations": "fastapi-microservice"}
        )
        provider = TracerProvider(resource=resource)

        # Uses standard gRPC collector protocol; reads OTEL_EXPORTER_OTLP_ENDPOINT from ECS env
        processor = BatchSpanProcessor(OTLPSpanExporter())
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)

        # Instrument FastAPI (Extracts the trace context from incoming Django HTTP headers)
        FastAPIInstrumentor.instrument_app(fastapi_app)
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

# Prometheus Metrics Exposer (Runs cleanly alongside OTel Tracing)
Instrumentator().instrument(app).expose(app)
