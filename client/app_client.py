import json
import zlib
import hashlib
import threading
from socket import socket
from datetime import datetime as dt


class Application:
    def __init__(self, host, port, buffersize):
        self._host = host
        self._port = port
        self._buffersize = buffersize

        self._client = socket()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            if exc_type is KeyboardInterrupt:
                print('Client shutdown')
            else:
                print('Client closed with error')
        else:
            print('Client shutdown')
        self._client.close()
        return True

    def read(self):
        response = self._client.recv(self._buffersize)
        server_response = zlib.decompress(response)
        print(server_response.decode())

    def bind(self):
        self._client.connect((self._host, self._port))
        print('Client was started')

    def write(self):
        hash_obj = hashlib.sha256()
        hash_obj.update(str(dt.now().timestamp()).encode())

        action = input('Enter action: ')
        data = input('Enter message: ')

        if 'update' in action:
            id_el = input('Enter id_el: ')
            request = {
                'action': action,
                'id_el': id_el,
                'data': data,
                'token': hash_obj.hexdigest(),
                'time': dt.now().timestamp()
            }
        elif 'delete' in action:
            print(action)
            id_el = input('Enter id_el: ')
            request = {
                'action': action,
                'id_el': id_el,
                'data': data,
                'token': hash_obj.hexdigest(),
                'time': dt.now().timestamp()
            }
        else:
            request = {
                'action': action,
                'data': data,
                'token': hash_obj.hexdigest(),
                'time': dt.now().timestamp()
            }

        client_request = json.dumps(request)
        server_request = zlib.compress(client_request.encode())

        self._client.send(server_request)
        print(f'Client send data: {data}')

    def start(self):
        read_thread = threading.Thread(target=self.read)
        read_thread.start()
        while True:
            self.write()
