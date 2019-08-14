import logging
import select
import threading
from socket import socket


class Application:
    def __init__(self, host, port, buffersize, handle):
        self._host = host
        self._port = port
        self._buffersize = buffersize
        self._handle = handle

        self._server = socket()
        self._connections = list()
        self._requests = list()

    def bind(self, backlog=5):
        self._server.bind((self._host, self._port))
        self._server.setblocking(False)
        self._server.listen(backlog)

    def accept(self):
        try:
            client, address = self._server.accept()
        except:
            pass
        else:
            self._connections.append(client)
            logging.info(f'Client was connected with {address[0]}:{address[1]} | Connections: {self._connections}')

    def read(self, sock):
        try:
            client_request = sock.recv(self._buffersize)
        except Exception:
            self._connections.remove(sock)
        else:
            if client_request:
                self._requests.append(client_request)

    def write(self, sock, response):
        try:
            sock.send(response)
        except Exception:
            self._connections.remove(sock)

    def start(self):
        try:
            logging.info(f'Server was started with {self._host}:{self._port}')

            while True:
                self.accept()

                rlist, wlist, xlist = select.select(self._connections, self._connections, self._connections, 0)

                for r in rlist:
                    read_thread = threading.Thread(target=self.read, args=(r))
                    read_thread.start()

                if self._requests:
                    client_request = self._requests.pop()
                    client_response = self._handle(client_request)

                    for w in wlist:
                        write_thread = threading.Thread(target=self.write, args=(w, client_response))
                        write_thread.start()

        except KeyboardInterrupt:
            logging.info('Server shutdown')
