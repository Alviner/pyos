from pyos8 import ReadWait, WriteWait
class Socket:
    def __init__(self, sock):
        self._sock = sock

    def accept(self):
        yield ReadWait(self._sock)
        client, addr = self._sock.accept()
        yield Socket(client), addr

    def send(self, buffer):
        while buffer:
            yield WriteWait(self._sock)
            length = self._sock.send(buffer)
            buffer = buffer[length:]

    def recv(self, maxbytes):
        yield ReadWait(self._sock)
        yield self._sock.recv(maxbytes)

    def close(self):
        yield self._sock.close()

