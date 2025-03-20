from ..checksum import checksum
from ..last_error import LastError
from ..regoerror import RegoError
from .decoder import Decoder


class AbstractDecoder(Decoder):
    def _convert(self, buffer: bytes) -> int | LastError | None:
        raise NotImplementedError

    def decode(self, buffer: bytes) -> int | LastError | None:
        if self.length < 1 or len(buffer) != self.length:
            raise RegoError(f"Unexpected size of '{buffer.hex()}'; expecting: {self.length}, got: {len(buffer)}")

        if buffer[0] != 0x01:
            raise RegoError(f"Invalid header for '{buffer.hex()}'")

        if self.length > 1 and checksum(buffer[1 : self.length - 1]) != buffer[self.length - 1]:
            raise RegoError(f"Invalid crc of '{buffer.hex()}'")

        return self._convert(buffer)
