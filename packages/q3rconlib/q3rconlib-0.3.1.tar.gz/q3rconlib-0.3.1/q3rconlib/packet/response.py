from .packet import Packet


class Response(Packet):
    @property
    def header(self) -> bytes:
        return Packet.MAGIC + 'print\n'.encode()

    def decode(self, resp: bytes) -> str:
        return resp.removeprefix(self.header).decode()
