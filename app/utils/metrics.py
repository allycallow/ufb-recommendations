from prometheus_client import Counter, Histogram

grpc_requests_total = Counter(
    "ufb_recommendations_grpc_requests_total",
    "Total number of gRPC requests handled, by method and status code",
    ["grpc_method", "grpc_code"],
)

grpc_request_duration_seconds = Histogram(
    "ufb_recommendations_grpc_request_duration_seconds",
    "Latency of gRPC requests in seconds",
    ["grpc_method"],
)
