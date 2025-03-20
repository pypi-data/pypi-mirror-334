from typing import Dict, Any, Optional
from neongram.parser.tl_object import TLFunction


class AuthSendCode(TLFunction):
    def __init__(self):
        super().__init__(
            "auth.sendCode",
            0xA677244F,
            [
                {"name": "phone_number", "type": "string"},
                {"name": "api_id", "type": "int"},
                {"name": "api_hash", "type": "string"},
                {"name": "settings", "type": "CodeSettings"},
            ],
            "auth.SentCode"
        )

class AuthSignIn(TLFunction):
    def __init__(self):
        super().__init__(
            "auth.signIn",
            0x8D52A951,
            [
                {"name": "phone_number", "type": "string"},
                {"name": "phone_code_hash", "type": "string"},
                {"name": "phone_code", "type": "string"},
                {"name": "password", "type": "string", "optional": True},
            ],
            "auth.Authorization"
        )

class AuthImportBotAuthorization(TLFunction):
    def __init__(self):
        super().__init__(
            "auth.importBotAuthorization",
            0x67A3FF2C,
            [
                {"name": "api_id", "type": "int"},
                {"name": "api_hash", "type": "string"},
                {"name": "bot_auth_token", "type": "string"},
            ],
            "auth.Authorization"
        )

class UsersGetUsers(TLFunction):
    def __init__(self):
        super().__init__(
            "users.getUsers",
            0x0D91A548,
            [
                {"name": "id", "type": "Vector<InputUser>"},
            ],
            "Vector<User>"
        )


class MessagesSendMessage(TLFunction):
    def __init__(self):
        super().__init__("messages.sendMessage", 0x6f5554bb, [
            {"name": "peer", "type": "InputPeer"},
            {"name": "message", "type": "string"},
            {"name": "random_id", "type": "long"},
            {"name": "reply_to_msg_id", "type": "int", "optional": True}
        ], "Updates")


class UpdatesGetState(TLFunction):
    def __init__(self):
        super().__init__("updates.getState", 0xedd4882a, [], "updates.State")


class MessagesGetHistory(TLFunction):
    def __init__(self):
        super().__init__("messages.getHistory", 0xafa92846, [
            {"name": "peer", "type": "InputPeer"},
            {"name": "offset_id", "type": "int"},
            {"name": "offset_date", "type": "int"},
            {"name": "add_offset", "type": "int"},
            {"name": "limit", "type": "int"},
            {"name": "max_id", "type": "int", "optional": True},
            {"name": "min_id", "type": "int", "optional": True}
        ], "messages.Messages")


class AccountGetPassword(TLFunction):
    def __init__(self):
        super().__init__("account.getPassword", 0x548a30f5, [], "account.Password")


class AccountUpdatePasswordSettings(TLFunction):
    def __init__(self):
        super().__init__("account.updatePasswordSettings", 0xb60a24ed, [
            {"name": "password", "type": "InputCheckPasswordSRP"},
            {"name": "new_settings", "type": "account.PasswordInputSettings"}
        ], "Bool")


class ChannelsJoinChannel(TLFunction):
    def __init__(self):
        super().__init__("channels.joinChannel", 0x24b524c5, [
            {"name": "channel", "type": "InputChannel"}
        ], "Updates")