import yaml
from socket import socket
from argparse import ArgumentParser

import json

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

try:
    server = socket()
    server.bind((base_settings.get('host'), base_settings.get('port')))
    server.listen(5)

    print(f'Server was started with {host}:{port}')

    while True:
        client, address = server.accept()
        print(f'Client was connected with {address[0]}:{address[1]}')
        client_request = client.recv(base_settings.get('buffersize'))
        request = json.loads(client_request.decode())

        if validate_request(request):
            action = request.get('action')
            controller = resolve(action)

            if controller:
                try:
                    print(f'Controller {action} is resolved with request: {client_request.decode()}')
                    response = controller(request)
                except Exception as err:
                    print(f'Controller {action} error: {err}')
                    response = make_response(request, 500, 'internal server error')
            else:
                print(f'Controller {action} not found')
                response = make_response(request, 404, f'Action with name {action} not supported')
        else:
            print(f'Controller wrong request: {request}')
            response = make_response(request, 400, 'wrong request')

        client.send(
            json.dumps(response).encode()
        )
        client.close()

except KeyboardInterrupt:
    print('Server shutdown')
