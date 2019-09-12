import json
import logging

from .resolvers import resolve
from .protocol import validate_request, make_response
from .middlewares import compression_middleware
from .security.middlewares import encryption_middleware


@compression_middleware
@encryption_middleware
def handle_default_request(raw_request):
    request = json.loads(raw_request.decode())

    if validate_request(request):
        action = request.get('action')
        controller = resolve(action)

        if controller:
            try:
                logging.debug(f'Controller {action} is resolved with request: {request}')
                response = controller(request)
            except Exception as err:
                logging.critical(f'Controller {action} error: {err}', exc_info=err)
                response = make_response(request, 500, 'internal server error')
        else:
            logging.error(f'Controller {action} not found')
            response = make_response(request, 404, f'Action with name {action} not supported')
    else:
        logging.error(f'Controller wrong request: {request}')
        response = make_response(request, 400, 'wrong request')

    return json.dumps(response).encode()
