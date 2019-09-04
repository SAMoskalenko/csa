import zlib
from functools import wraps


def compression_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        client_request = zlib.decompress(request)
        client_response = func(client_request, *args, **kwargs)
        return zlib.compress(client_response)

    return wrapper
