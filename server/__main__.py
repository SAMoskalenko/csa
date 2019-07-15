import yaml
import json
import logging

from socket import socket
from argparse import ArgumentParser

from protocol import validate_request, make_response
from resolvers import resolve

parser = ArgumentParser()

parser.add_argument(
    '-s', '--settings', type=str,
    required=False, help='Settings file path'
)

args = parser.parse_args()

base_settings = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024
}

if args.settings:
    with open(args.settings) as file:
        settings = yaml.load(file, Loader=yaml.Loader)
        base_settings.update(settings)

host, port = base_settings.get('host'), base_settings.get('port')

logger = logging.getLogger('server_main')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

hendler = logging.FileHandler('server_main.log')
hendler.setFormatter(formatter)
hendler.setLevel(logging.DEBUG)

logger.addHandler(hendler)

try:
    server = socket()
    server.bind((base_settings.get('host'), base_settings.get('port')))
    server.listen(5)

    logger.info(f'Server was started with {host}:{port}')

    while True:
        client, address = server.accept()
        logger.info(f'Client was connected with {address[0]}:{address[1]}')
        client_request = client.recv(base_settings.get('buffersize'))
        request = json.loads(client_request.decode())

        if validate_request(request):
            action = request.get('action')
            controller = resolve(action)

            if controller:
                try:
                    logger.debug(f'Controller {action} is resolved with request: {client_request.decode()}')
                    response = controller(request)
                except Exception as err:
                    logger.critical(f'Controller {action} error: {err}')
                    response = make_response(request, 500, 'internal server error')
            else:
                logger.error(f'Controller {action} not found')
                response = make_response(request, 404, f'Action with name {action} not supported')
        else:
            logger.error(f'Controller wrong request: {request}')
            response = make_response(request, 400, 'wrong request')

        client.send(
            json.dumps(response).encode()
        )
        client.close()

except KeyboardInterrupt:
    logger.info('Server shutdown')
