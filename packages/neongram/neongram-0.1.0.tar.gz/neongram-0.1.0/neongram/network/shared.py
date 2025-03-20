import asyncio
import os
from typing import Optional

class Connection:
    def __init__(self, host: str, port: int, dc_id: int):
        self.dc_id = dc_id
        from neongram.network.transport import Transport
        self.transport = Transport(host, port)
        from neongram.network.mtproto_sender import MTProtoSender
        self.sender = MTProtoSender(self)
        from neongram.network.mtproto_receiver import MTProtoReceiver
        self.receiver = MTProtoReceiver(self)
        self.session_id: Optional[int] = None
        self.server_salt: Optional[int] = None
        self.auth_key: Optional[bytes] = None
        self.sequence = 0
        self.lock = asyncio.Lock()

    async def connect(self) -> None:
        await self.transport.connect()
        self.session_id = await self._generate_session_id()
        await self.receiver.start()

    async def _generate_session_id(self) -> int:
        return int.from_bytes(await asyncio.get_event_loop().run_in_executor(None, os.urandom, 8), "little")

    async def send(self, data: bytes) -> None:
        await self.sender.send(data)

    async def receive(self) -> bytes:
        return await self.receiver.receive()

    async def close(self) -> None:
        await self.receiver.stop()
        await self.transport.close()

    async def next_sequence(self) -> int:
        async with self.lock:
            current = self.sequence
            self.sequence += 1
            return current