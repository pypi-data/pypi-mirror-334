# neongram/client/client.py
from typing import Optional, Dict, Any, Callable, Union
import asyncio
import platform
import os
import logging
from neongram.network.shared import Connection
from neongram.client.session import Session
from neongram.parser.tl_object import TLFunction
from neongram.parser.tl_parser import TLParser
from neongram.client.auth import Auth
from neongram import __version__

log = logging.getLogger(__name__)

class NeonClient:
    def __init__(
        self,
        name: str,
        api_id: Optional[Union[int, str]] = None,
        api_hash: Optional[str] = None,
        app_version: str = "Neon 1.0.0",
        device_model: str = f"{platform.python_implementation()} {platform.python_version()}",
        system_version: str = f"{platform.system()} {platform.release()}",
        lang_code: str = "en",
        ipv6: bool = False,
        proxy: Optional[Dict[str, Any]] = None,
        test_mode: bool = False,
        bot_token: Optional[str] = None,
        session_string: Optional[str] = None,
        in_memory: bool = False,
        phone_number: Optional[str] = None,
        phone_code: Optional[str] = None,
        password: Optional[str] = None,
        workers: int = min(32, (os.cpu_count() or 1) + 4),
        workdir: str = os.getcwd(),
        plugins: Optional[Dict[str, Any]] = None,
        parse_mode: str = "both",
        no_updates: bool = False,
        takeout: bool = False,
        sleep_threshold: int = 10,
        hide_password: bool = False,
        max_concurrent_transmissions: int = 1,
    ):
        self.name = name
        self.api_id = int(api_id) if api_id else None
        self.api_hash = api_hash
        self.app_version = app_version
        self.device_model = device_model
        self.system_version = system_version
        self.lang_code = lang_code
        self.ipv6 = ipv6
        self.proxy = proxy
        self.test_mode = test_mode
        self.bot_token = bot_token
        self.session = Session(name, session_string, in_memory, workdir)
        self.phone_number = phone_number
        self.phone_code = phone_code
        self.password = password
        self.workers = workers
        self.plugins = plugins or {}
        self.parse_mode = parse_mode
        self.no_updates = no_updates or takeout
        self.takeout = takeout
        self.sleep_threshold = sleep_threshold
        self.hide_password = hide_password
        self.max_concurrent_transmissions = max_concurrent_transmissions
        self.dc_id = 2  # Default DC; can be updated dynamically
        self.connection = Connection(self.dc_id, test_mode, ipv6, proxy)
        self.auth = Auth(self)
        schema_path = os.path.join(workdir, "schema", "api.tl")
        self.parser = TLParser(schema_path)
        self.running = False
        self.loop: Optional[asyncio.AbstractEventLoop] = None

    async def start(self) -> None:
        self.loop = asyncio.get_event_loop()
        await self.connection.connect()
        if not self.session.auth_key or not self.session.server_salt:
            from neongram.parser.tl_object import TLFunction
            req_pq = TLFunction("req_pq_multi", 0xBE7E8EF1, [{"name": "nonce", "type": "int128"}], "ResPQ")
            import os
            nonce = int.from_bytes(os.urandom(16), "little")
            req_pq.values["nonce"] = nonce
            await self.invoke(req_pq)  # Placeholder; full DH exchange needed
            await self.auth.authenticate()
            self.connection.auth_key = self.session.auth_key
            self.connection.server_salt = self.session.server_salt
        self.running = True
        print(f"neongram started successfully created by nobitha with the version of: {__version__}")

    async def stop(self) -> None:
        self.running = False
        if self.connection:
            await self.connection.close()
        if not self.session.in_memory:
            self.session.save()

    async def invoke(self, function: TLFunction) -> bytes:
        if not self.running:
            raise ConnectionError("Client not started")
        serialized = function.serialize()
        await self.connection.send(serialized)
        return await self.connection.receive()

    async def get_me(self) -> Dict[str, Any]:
        from neongram.methods import UsersGetUsers
        request = UsersGetUsers()
        request.values["id"] = [{"_": "inputUserSelf"}]
        response = await self.invoke(request)
        return {"raw": response.hex()}  # Placeholder; add deserialization

    def run(self, coro: Callable) -> None:
        if not self.loop:
            self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(coro)