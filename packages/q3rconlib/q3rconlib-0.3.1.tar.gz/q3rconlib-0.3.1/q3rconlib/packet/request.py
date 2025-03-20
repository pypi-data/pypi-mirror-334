from .packet import Packet


class Request(Packet):
    def __init__(self, password: str):
        self.password = password

    @property
    def header(self) -> bytes:
        return Packet.MAGIC + 'rcon'.encode()

    def encode(self, cmd) -> bytes:
        return self.header + f' {self.password} {cmd}'.encode()
