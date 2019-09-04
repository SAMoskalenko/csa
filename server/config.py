class ConfigProperty:
    def __init__(self, name, default=None):
        self._name = f'_{name}'
        self._default = default

    def __get__(self, instance, cls):
        return getattr(instance, self._name, self._default)


class Config:
    def __init__(self, host, port, buffersize):
        self._host = host
        self._port = port
        self._buffersize = buffersize

    host = ConfigProperty('host', 'localhost')
    port = ConfigProperty('port', 8000)
    buffersize = ConfigProperty('buffersize', 1024)

