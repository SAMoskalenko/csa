import yaml
import logging
import select
import threading
from socket import socket
from argparse import ArgumentParser
from handlers import handle_default_request


def read(sock, connections, requests, bufersize):
    try:
        client_request = sock.recv(bufersize)
    except Exception:
        connections.remove(sock)
    else:
        requests.append(client_request)


def write(sock, connections, response):
    try:
        sock.send(response)
    except Exception:
        connections.remove(sock)


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
            read_thread = threading.Thread(target=read,
                                           args=(r, connections, requests, base_settings.get('buffersize')))
            read_thread.start()

        if requests:
            client_request = requests.pop()
            client_response = handle_default_request(client_request)

            for w in wlist:
                write_thread = threading.Thread(target=write,
                                                args=(w, connections, client_response))
                write_thread.start()

except KeyboardInterrupt:
    logging.info('Server shutdown')
