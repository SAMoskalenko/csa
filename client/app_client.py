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

    def read(self):
        while True:
            response = self._client.recv(self._buffersize)
            server_response = zlib.decompress(response)
            print(server_response.decode())

    def bind(self):
        self._client.connect((self._host, self._port))
        print('Client was started')

    def start(self):
        try:
            read_thread = threading.Thread(target=self.read, args=())
            read_thread.start()

            while True:
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

                self._client.send(server_request)
                print(f'Client send data: {data}')

        except KeyboardInterrupt:
            self._client.close()
            print('Client shutdown')
