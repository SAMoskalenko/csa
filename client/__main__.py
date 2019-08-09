import yaml
import json
import zlib
import hashlib
import threading
from socket import socket
from argparse import ArgumentParser
from datetime import datetime as dt


def read(sock, buffersize):
    while True:
        response = sock.recv(buffersize)
        server_response = zlib.decompress(response)
        print(server_response.decode())


parser = ArgumentParser()

parser.add_argument(
    '-s', '--settings', type=str,
    required=False, help='Settings file path'
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

try:
    while True:
        read_thread = threading.Thread(target=read, args=(client, base_settings.get('buffersize')))
        read_thread.start()

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

        client.send(server_request)
        print(f'Client send data: {data}')
except KeyboardInterrupt:
    client.close()
    print('Client shutdown')
