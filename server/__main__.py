import yaml
from socket import socket
from argparse import ArgumentParser

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
        request = client.recv(base_settings.get('buffersize'))
        print(f'client send message: {request.decode()}')
        client.send(request)
        client.close()
except KeyboardInterrupt:
    print('Server shutdown')