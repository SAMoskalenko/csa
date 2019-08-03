import yaml
import json
import zlib
import hashlib
from socket import socket
from argparse import ArgumentParser
from datetime import datetime as dt

parser = ArgumentParser()

parser.add_argument(
    '-s', '--settings', type=str,
    required=False, help='Settings file path'
)

parser.add_argument(
    '-m', '--mode', type=str, default='r', required=False,
)

args = parser.parse_args()

base_settings = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024,
}

if args.settings:
    with open(args.settings) as file:
        settings = yaml.load(file, Loader=yaml.Loader)
        base_settings.update(settings)

client = socket()
client.connect((base_settings.get('host'), base_settings.get('port')))

print('Client was started')


def write(sock):
    hash_obj = hashlib.sha256()
    hash_obj.update(str(dt.now().timestamp()).encode())

    action = input('Enter action: ')
    data = input('Enter message: ')

    request = {
        'action': action,
        'data': data,
        'token': hash_obj.hexdigest(),
        'time': dt.now().timestamp()
    }

    client_request = json.dumps(request)
    server_request = zlib.compress(client_request.encode())

    sock.send(server_request)
    print(f'Client send data: {data}')


def read(sock):
    response = sock.recv(base_settings.get('buffersize'))
    server_response = zlib.decompress(response)
    print(server_response.decode())


try:
    while True:
        if args.mode == 'w':
            write(client)
        elif args.mode == 'r':
            read(client)
except KeyboardInterrupt:
    client.close()
    print('Client shutdown')
