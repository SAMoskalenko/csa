import zlib
import json
import hmac
from functools import wraps

from protocol import make_response
from auth.models import User, Session


def compression_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        client_request = zlib.decompress(request)
        client_response = func(client_request, *args, **kwargs)
        return zlib.compress(client_response)

    return wrapper

# def encryption_middleware(func):
#     @wraps(func)
#     def wrapper(request, *args, **kwargs):
#         encrypted_request = json.loads(request)
#         key = encrypted_request.get('key')
#         data = encrypted_request.get('data')
#         cypher = AES.new(key, AES.MODE_CBC)
#         decrypted_data = cypher.decrypt(data)
#         decrypted_request = encrypted_request.copy()
#         decrypted_request['data'] = decrypted_data
#         client_request = json.dumps(decrypted_request).encode()
#
#         client_response = func(client_request, *args, **kwargs)
#
#         decrypted_response = json.loads(client_response)
#         decrypted_data = decrypted_response.get('data')
#         encrypted_data = cypher.encrypt(decrypted_data)
#         encrypted_response = decrypted_response.copy()
#         encrypted_response['data'] = encrypted_data
#         print(json.dumps(encrypted_response))
#
#         return json.dumps(encrypted_response).encode()
#
#     return wrapper


def encryption_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        client_response = func(request, *args, **kwargs)
        return client_response

    return wrapper


def auth_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        authentificated = True

        request_obj = json.loads(request)
        login = request_obj.get('login')
        token = request_obj.get('token')
        time = request_obj.get('time')

        session = Session()
        user = session.query(User).filter_by(name=login).first()
        if user:
            digest = hmac.new(time, user.password)

            if hmac.compare_digest(digest, token):
                authentificated = False
        else:
            authentificated = False

        if authentificated:
            return func(request, *args, **kwargs)
        response = make_response(request, 401, 'Access denied')
        return json.dumps(response).encode()

    return wrapper
