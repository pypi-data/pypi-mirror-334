import grpc

_grpc_to_status_mapping = {
    grpc.StatusCode.OK: 0,
    grpc.StatusCode.INVALID_ARGUMENT: 400,
    grpc.StatusCode.UNAUTHENTICATED: 401,
    grpc.StatusCode.PERMISSION_DENIED: 403,
    grpc.StatusCode.NOT_FOUND: 404,
    grpc.StatusCode.ABORTED: 409,
    grpc.StatusCode.FAILED_PRECONDITION: 412,
    grpc.StatusCode.OUT_OF_RANGE: 416,
    grpc.StatusCode.ALREADY_EXISTS: 409,
    grpc.StatusCode.RESOURCE_EXHAUSTED: 429,
    grpc.StatusCode.CANCELLED: 499,
    grpc.StatusCode.INTERNAL: 500,
    grpc.StatusCode.DATA_LOSS: 500,
    grpc.StatusCode.UNKNOWN: 500,
    grpc.StatusCode.UNIMPLEMENTED: 501,
    grpc.StatusCode.DEADLINE_EXCEEDED: 504,
    grpc.StatusCode.UNAVAILABLE: 503,
}


def to_status_code(grpc_code: grpc.StatusCode) -> int:
    return _grpc_to_status_mapping.get(grpc_code, 500)


_status_to_grpc_mapping = {
    0: grpc.StatusCode.OK,
    400: grpc.StatusCode.INVALID_ARGUMENT,
    401: grpc.StatusCode.UNAUTHENTICATED,
    403: grpc.StatusCode.PERMISSION_DENIED,
    404: grpc.StatusCode.NOT_FOUND,
    409: grpc.StatusCode.ABORTED,
    412: grpc.StatusCode.FAILED_PRECONDITION,
    416: grpc.StatusCode.OUT_OF_RANGE,
    429: grpc.StatusCode.RESOURCE_EXHAUSTED,
    499: grpc.StatusCode.CANCELLED,
    500: grpc.StatusCode.INTERNAL,
    501: grpc.StatusCode.UNIMPLEMENTED,
    503: grpc.StatusCode.UNAVAILABLE,
    504: grpc.StatusCode.DEADLINE_EXCEEDED,
}


def from_status_code(status_code: int) -> grpc.StatusCode:
    return _status_to_grpc_mapping.get(status_code, grpc.StatusCode.UNKNOWN)
