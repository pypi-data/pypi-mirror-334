from typing import Optional
import json
import os


class Session:
    """Manages persistent session state for NeonClient.

    Args:
        name (str): Unique session identifier.
        session_string (str, optional): String representation of session data for in-memory loading.
        in_memory (bool): Whether to store session in memory only.
        workdir (str): Directory for session file storage.
    """

    def __init__(
        self,
        name: str,
        session_string: Optional[str] = None,
        in_memory: bool = False,
        workdir: str = os.getcwd(),
    ):
        self.name = name
        self.in_memory = in_memory
        self.session_file = os.path.join(workdir, f"{name}.txt") if not in_memory else None
        self.auth_key: Optional[bytes] = None
        self.server_salt: Optional[int] = None
        self.session_id: Optional[int] = None
        if session_string:
            self._load_from_string(session_string)
        elif not in_memory:
            self._load_from_file()

    def save(self) -> None:
        """Persist session data to file if not in-memory."""
        if self.in_memory:
            return
        data = {
            "auth_key": self.auth_key.hex() if self.auth_key else None,
            "server_salt": self.server_salt,
            "session_id": self.session_id,
        }
        with open(self.session_file, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def gen_session_string(self) -> str:
        """Generate a string representation of the session.

        Returns:
            str: Session string for in-memory use.
        """
        data = {
            "auth_key": self.auth_key.hex() if self.auth_key else None,
            "server_salt": self.server_salt,
            "session_id": self.session_id,
        }
        return json.dumps(data)

    def _load_from_file(self) -> None:
        if os.path.exists(self.session_file):
            with open(self.session_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.auth_key = bytes.fromhex(data["auth_key"]) if data["auth_key"] else None
                self.server_salt = data["server_salt"]
                self.session_id = data["session_id"]

    def _load_from_string(self, session_string: str) -> None:
        data = json.loads(session_string)
        self.auth_key = bytes.fromhex(data["auth_key"]) if data["auth_key"] else None
        self.server_salt = data["server_salt"]
        self.session_id = data["session_id"]