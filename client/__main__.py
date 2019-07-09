import yaml
from socket import socket
from argparse import ArgumentParser
from datetime import datetime as dt

import json


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

client = socket()
client.connect((base_settings.get('host'), base_settings.get('port')))

print('Client was started')

action = input('Enter action: ')
data = input('Enter message: ')

request = {
    'action': action,
    'data': data,
    'time': dt.now().timestamp()
}

client_request = json.dumps(request)

client.send(client_request.encode())
print(f'Client send data: {data}')

response = client.recv(base_settings.get('buffersize'))

print(response.decode())
