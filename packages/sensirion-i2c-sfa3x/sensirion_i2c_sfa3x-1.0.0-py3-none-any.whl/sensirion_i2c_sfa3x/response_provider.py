import struct
import sensirion_driver_adapters.mocks.response_provider as rp


class Sfa3xResponseProvider(rp.ResponseProvider):

    RESPONSE_MAP = {0xd060: struct.pack('>32s', rp.random_ascii_string(32))}

    def get_id(self) -> str:
        return 'Sfa3xResponseProvider'

    def handle_command(self, cmd_id: int, data: bytes, response_length: int) -> bytes:
        return self.RESPONSE_MAP.get(cmd_id, rp.random_bytes(response_length))
