import logging
import socket
import asyncio
import ssl
from typing import Optional
from neongram.network.transport import TCPAbridged
from neongram.network.data_center import DataCenter
from neongram.utils.binary_writer import BinaryWriter

log = logging.getLogger(__name__)

class Connection:
    MAX_CONNECTION_ATTEMPTS = 3

    def __init__(self, dc_id: int, test_mode: bool, ipv6: bool, proxy: Optional[dict] = None, media: bool = False):
        self.dc_id = dc_id
        self.test_mode = test_mode
        self.ipv6 = ipv6
        self.proxy = proxy
        self.media = media
        self.host, self.port = DataCenter.get_address(dc_id, test_mode, ipv6, media)
        self.protocol: Optional[TCPAbridged] = None
        self.auth_key: Optional[bytes] = None
        self.server_salt: Optional[int] = None

    async def connect(self):
        for i in range(Connection.MAX_CONNECTION_ATTEMPTS):
            self.protocol = TCPAbridged(self.ipv6, self.proxy)

            try:
                log.info(f"Connecting to {self.host}:{self.port}...")
                await self.protocol.connect((self.host, self.port))
            except OSError as e:
                log.warning(f"Unable to connect due to network issues: {e}")
                await self.protocol.close()
                await asyncio.sleep(1)
            else:
                log.info(f"Connected to {'Test' if self.test_mode else 'Production'} DC{self.dc_id}"
                         f"{' (media)' if self.media else ''} - IPv{'6' if self.ipv6 else '4'}")
                break
        else:
            log.warning("Connection failed! Max retries reached.")
            raise ConnectionError("Failed to establish connection after max retries")

    async def send(self, data: bytes):
        if not self.protocol:
            raise ConnectionError("No active connection")
        writer = BinaryWriter()
        writer.write_int(0xeeeeeeee)  # MTProto header
        writer.write_int(len(data))   # Length of payload
        writer.write_bytes(data)      # Payload
        await self.protocol.send(writer.get_bytes())

    async def receive(self) -> Optional[bytes]:
        if not self.protocol:
            raise ConnectionError("No active connection")
        return await self.protocol.recv()

    async def close(self):
        if self.protocol:
            await self.protocol.close()
            log.info("Disconnected")