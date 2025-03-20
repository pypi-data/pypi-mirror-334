from typing import Callable, Dict, List, Optional
from ..parser.tl_object import TLObject
from ..filters import Filter
from ..enums import UpdateType
from ..client import NeonClient
from ..errors.exceptions import MTProtoException


class Handler:
    """

    Args:
        callback (Callable[[TLObject, NeonClient], None]): Function to execute when the handler is triggered.
        filter (Filter, optional): Filter to apply before invoking the callback. Defaults to None.
    """

    def __init__(self, callback: Callable[[TLObject, NeonClient], None], filter: Optional[Filter] = None):
        self.callback = callback
        self.filter = filter or Filter()

    async def handle(self, obj: TLObject, client: NeonClient) -> None:
        if self.filter(obj):
            await self.callback(obj, client)


class MessageHandler(Handler):
    """

    Args:
        callback (Callable[[TLObject, NeonClient], None]): Function to execute for new messages.
        filter (Filter, optional): Filter to apply to messages. Defaults to None.
    """

    async def handle(self, obj: TLObject, client: NeonClient) -> None:
        if hasattr(obj, "_") and obj._ == UpdateType.NEW_MESSAGE.value and "message" in obj.values:
            await super().handle(obj, client)


class EditedMessageHandler(Handler):
    """

    Args:
        callback (Callable[[TLObject, NeonClient], None]): Function to execute for edited messages.
        filter (Filter, optional): Filter to apply to edited messages. Defaults to None.
    """

    async def handle(self, obj: TLObject, client: NeonClient) -> None:
        if hasattr(obj, "_") and obj._ == "updateEditMessage" and "message" in obj.values:
            await super().handle(obj, client)


class DeletedMessagesHandler(Handler):
    """

    Args:
        callback (Callable[[TLObject, NeonClient], None]): Function to execute for deleted messages.
        filter (Filter, optional): Filter to apply to deleted messages updates. Defaults to None.
    """

    async def handle(self, obj: TLObject, client: NeonClient) -> None:
        if hasattr(obj, "_") and obj._ == UpdateType.DELETE_MESSAGES.value:
            await super().handle(obj, client)


class CallbackQueryHandler(Handler):
    """

    Args:
        callback (Callable[[TLObject, NeonClient], None]): Function to execute for callback queries.
        filter (Filter, optional): Filter to apply to callback queries. Defaults to None.
    """

    async def handle(self, obj: TLObject, client: NeonClient) -> None:
        if hasattr(obj, "_") and obj._ == "updateCallbackQuery":
            await super().handle(obj, client)


class InlineQueryHandler(Handler):
    """

    Args:
        callback (Callable[[TLObject, NeonClient], None]): Function to execute for inline queries.
        filter (Filter, optional): Filter to apply to inline queries. Defaults to None.
    """

    async def handle(self, obj: TLObject, client: NeonClient) -> None:
        if hasattr(obj, "_") and obj._ == "updateInlineQuery":
            await super().handle(obj, client)


class ChosenInlineResultHandler(Handler):
    """

    Args:
        callback (Callable[[TLObject, NeonClient], None]): Function to execute for chosen inline results.
        filter (Filter, optional): Filter to apply to chosen inline results. Defaults to None.
    """

    async def handle(self, obj: TLObject, client: NeonClient) -> None:
        if hasattr(obj, "_") and obj._ == "updateChosenInlineResult":
            await super().handle(obj, client)


class ChatJoinRequestHandler(Handler):
    """

    Args:
        callback (Callable[[TLObject, NeonClient], None]): Function to execute for chat join requests.
        filter (Filter, optional): Filter to apply to chat join requests. Defaults to None.
    """

    async def handle(self, obj: TLObject, client: NeonClient) -> None:
        if hasattr(obj, "_") and obj._ == "updateChatJoinRequest":
            await super().handle(obj, client)


class ChatMemberUpdatedHandler(Handler):
    """

    Args:
        callback (Callable[[TLObject, NeonClient], None]): Function to execute for chat member updates.
        filter (Filter, optional): Filter to apply to chat member updates. Defaults to None.
    """

    async def handle(self, obj: TLObject, client: NeonClient) -> None:
        if hasattr(obj, "_") and obj._ == "updateChatMember":
            await super().handle(obj, client)


class UserStatusHandler(Handler):
    """

    Args:
        callback (Callable[[TLObject, NeonClient], None]): Function to execute for user status updates.
        filter (Filter, optional): Filter to apply to user status updates. Defaults to None.
    """

    async def handle(self, obj: TLObject, client: NeonClient) -> None:
        if hasattr(obj, "_") and obj._ == UpdateType.USER_STATUS.value:
            await super().handle(obj, client)


class PollHandler(Handler):
    """

    Args:
        callback (Callable[[TLObject, NeonClient], None]): Function to execute for poll updates.
        filter (Filter, optional): Filter to apply to poll updates. Defaults to None.
    """

    async def handle(self, obj: TLObject, client: NeonClient) -> None:
        if hasattr(obj, "_") and obj._ == "updatePoll":
            await super().handle(obj, client)


class RawUpdateHandler(Handler):
    """

    Args:
        callback (Callable[[TLObject, NeonClient], None]): Function to execute for raw updates.
        filter (Filter, optional): Filter to apply to raw updates. Defaults to None.
    """

    async def handle(self, obj: TLObject, client: NeonClient) -> None:
        await super().handle(obj, client)


class DisconnectHandler(Handler):
    """

    Args:
        callback (Callable[[TLObject, NeonClient], None]): Function to execute on disconnection.
        filter (Filter, optional): Filter to apply to disconnection events. Defaults to None.
    """

    async def handle(self, obj: TLObject, client: NeonClient) -> None:
        if hasattr(obj, "_") and obj._ == "updateConnectionState" and obj.values.get("state") == "disconnected":
            await super().handle(obj, client)


class HandlerManager:
    """

    Args:
        client (NeonClient): The associated client instance.
    """

    def __init__(self, client: NeonClient):
        self.client = client
        self.handlers: List[Handler] = []

    def add_handler(self, handler: Handler) -> None:
        self.handlers.append(handler)

    def remove_handler(self, handler: Handler) -> bool:
        if handler in self.handlers:
            self.handlers.remove(handler)
            return True
        return False

    async def process_update(self, update: TLObject) -> None:
        for handler in self.handlers:
            try:
                await handler.handle(update, self.client)
            except MTProtoException:
                continue

    def get_handlers(self) -> List[Handler]:
        return self.handlers.copy()
