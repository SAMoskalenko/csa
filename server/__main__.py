import yaml
import logging

import select
from socket import socket
from argparse import ArgumentParser
from handlers import handle_default_request

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

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server_main.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

connections = []
requests = []

try:
    server = socket()
    server.bind((host, port))
    server.setblocking(False)
    server.listen(5)

    logging.info(f'Server was started with {host}:{port}')

    while True:
        try:
            client, address = server.accept()
            connections.append(client)
            logging.info(f'Client was connected with {address[0]}:{address[1]} | Connections: {connections}')
        except:
            pass

        rlist, wlist, xlist = select.select(connections, connections, connections, 0)

        for r in rlist:
            client_request = r.recv(base_settings.get('buffersize'))
            requests.append(client_request)

        if requests:
            client_request = requests.pop()
            client_response = handle_default_request(client_request)

            for w in wlist:
                w.send(client_response)

except KeyboardInterrupt:
    logging.info('Server shutdown')
