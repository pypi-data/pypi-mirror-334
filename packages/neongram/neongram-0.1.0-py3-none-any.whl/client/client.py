from typing import Optional, Dict, Any, Callable
import asyncio
import platform
import os
from neongram.network.shared import Connection
from .session import Session
from neongram.parser.tl_object import TLFunction
from neongram.parser.tl_parser import TLParser

class NeonClient:
    """
    Args:
        name (str): Unique identifier for this client instance.
        api_id (int | str, optional): Telegram API ID from my.telegram.org.
        api_hash (str, optional): Telegram API hash from my.telegram.org.
        app_version (str, optional): Application version string. Defaults to "Neon 1.0.0".
        device_model (str, optional): Device model string. Defaults to Python implementation and version.
        system_version (str, optional): OS version string. Defaults to platform system and release.
        lang_code (str, optional): ISO 639-1 language code. Defaults to "en".
        ipv6 (bool, optional): Use IPv6 for connections. Defaults to False.
        proxy (dict, optional): Proxy settings (e.g., {"scheme": "socks5", "hostname": "1.2.3.4", "port": 1234}).
        test_mode (bool, optional): Use Telegram test servers. Defaults to False.
        bot_token (str, optional): Bot API token for bot sessions.
        session_string (str, optional): Session string for in-memory loading.
        in_memory (bool, optional): Run session in memory without file persistence. Defaults to False.
        phone_number (str, optional): Phone number for automatic login.
        phone_code (str, optional): Phone code for test numbers.
        password (str, optional): Two-Step Verification password.
        workers (int, optional): Number of concurrent update workers. Defaults to min(32, CPU count + 4).
        workdir (str, optional): Working directory for session files. Defaults to current directory.
        plugins (dict, optional): Plugin configuration (e.g., {"root": "plugins"}).
        parse_mode (str, optional): Text parsing mode ("markdown", "html", or "both"). Defaults to "both".
        no_updates (bool, optional): Disable update handling. Defaults to False.
        takeout (bool, optional): Use a takeout session. Defaults to False.
        sleep_threshold (int, optional): Sleep threshold for flood waits in seconds. Defaults to 10.
        hide_password (bool, optional): Hide password input. Defaults to False.
        max_concurrent_transmissions (int, optional): Max concurrent uploads/downloads. Defaults to 1.
    """

    def __init__(
        self,
        name: str,
        api_id: Optional[int | str] = None,
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
        workers: int = min(32, os.cpu_count() or 1 + 4),
        workdir: str = os.getcwd(),
        plugins: Optional[Dict[str, Any]] = None,
        parse_mode: str = "both",
        no_updates: bool = False,
        takeout: bool = False,
        sleep_threshold: int = 10,
        hide_password: bool = False,
        max_concurrent_transmissions: int = 1,
    ):
        from neongram.client.auth import Auth  # Moved import here to avoid circular import
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
        self.host = "149.154.167.50" if not test_mode else "149.154.167.40"
        self.port = 443
        self.dc_id = 2
        self.connection = Connection(self.host, self.port, self.dc_id)
        self.auth = Auth(self)
        self.parser = TLParser(os.path.join(workdir, "schema", "api.tl"))
        self.running = False
        self.loop: Optional[asyncio.AbstractEventLoop] = None

    async def start(self) -> None:
        self.loop = asyncio.get_event_loop()
        await self.connection.connect()
        if not self.session.auth_key or not self.session.server_salt:
            await self.auth.authenticate()
            self.connection.auth_key = self.session.auth_key
            self.connection.server_salt = self.session.server_salt
        self.running = True

    async def stop(self) -> None:
        self.running = False
        await self.connection.close()
        if not self.session.in_memory:
            self.session.save()

    async def invoke(self, function: TLFunction) -> bytes:
        """Send a TL function request and receive the raw response.

        Args:
            function (TLFunction): The TL function to execute.

        Returns:
            bytes: Raw response data.
        """
        serialized = function.serialize()
        await self.connection.send(serialized)
        return await self.connection.receive()

    async def get_me(self) -> Dict[str, Any]:
        """Retrieve information about the current user.

        Returns:
            Dict[str, Any]: User data (simplified as raw response).
        """
        from neongram.methods import UsersGetUsers
        request = UsersGetUsers()
        request.values["id"] = [{"_": "inputUserSelf"}]
        response = await self.invoke(request)
        return {"raw": response.hex()}  # Placeholder; add deserialization for full data

    def run(self, coro: Callable) -> None:
        """Execute an async coroutine in the client's event loop.

        Args:
            coro: The coroutine to run.
        """
        if not self.loop:
            self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(coro)