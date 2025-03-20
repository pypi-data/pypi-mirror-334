from typing import Optional, List
from neongram.parser.tl_object import TLObject
from neongram.utils.binary_reader import BinaryReader
from neongram.utils.binary_writer import BinaryWriter
from neongram.types.channel.input_channel import InputChannel
from neongram.types.users.user import User


class ChatAdminRights:
    """Represents admin rights in a chat.

    Args:
        change_info (bool): Can change chat info.
        post_messages (bool): Can post messages.
        edit_messages (bool): Can edit messages.
        delete_messages (bool): Can delete messages.
        ban_users (bool): Can ban users.
        invite_users (bool): Can invite users.
        pin_messages (bool): Can pin messages.
        add_admins (bool): Can add new admins.
    """

    def __init__(self, change_info: bool = False, post_messages: bool = False, edit_messages: bool = False,
                 delete_messages: bool = False, ban_users: bool = False, invite_users: bool = False,
                 pin_messages: bool = False, add_admins: bool = False):
        self.change_info = change_info
        self.post_messages = post_messages
        self.edit_messages = edit_messages
        self.delete_messages = delete_messages
        self.ban_users = ban_users
        self.invite_users = invite_users
        self.pin_messages = pin_messages
        self.add_admins = add_admins

    def to_bytes(self) -> bytes:
        writer = BinaryWriter()
        flags = 0
        flags |= (1 << 0) if self.change_info else 0
        flags |= (1 << 1) if self.post_messages else 0
        flags |= (1 << 2) if self.edit_messages else 0
        flags |= (1 << 3) if self.delete_messages else 0
        flags |= (1 << 4) if self.ban_users else 0
        flags |= (1 << 5) if self.invite_users else 0
        flags |= (1 << 7) if self.pin_messages else 0
        flags |= (1 << 9) if self.add_admins else 0
        writer.write_int(flags)
        return writer.get_bytes()

    @classmethod
    def from_reader(cls, reader: BinaryReader) -> "ChatAdminRights":
        flags = reader.read_int()
        return cls(
            change_info=bool(flags & (1 << 0)),
            post_messages=bool(flags & (1 << 1)),
            edit_messages=bool(flags & (1 << 2)),
            delete_messages=bool(flags & (1 << 3)),
            ban_users=bool(flags & (1 << 4)),
            invite_users=bool(flags & (1 << 5)),
            pin_messages=bool(flags & (1 << 7)),
            add_admins=bool(flags & (1 << 9))
        )


class ChatBannedRights:
    """Represents banned rights in a chat.

    Args:
        view_messages (bool): Can view messages.
        send_messages (bool): Can send messages.
        send_media (bool): Can send media.
        send_stickers (bool): Can send stickers.
        send_gifs (bool): Can send GIFs.
        send_games (bool): Can send games.
        send_inline (bool): Can send inline messages.
        embed_links (bool): Can embed links.
        until_date (int): Duration of the ban (Unix timestamp).
    """

    def __init__(self, view_messages: bool = False, send_messages: bool = False, send_media: bool = False,
                 send_stickers: bool = False, send_gifs: bool = False, send_games: bool = False,
                 send_inline: bool = False, embed_links: bool = False, until_date: int = 0):
        self.view_messages = view_messages
        self.send_messages = send_messages
        self.send_media = send_media
        self.send_stickers = send_stickers
        self.send_gifs = send_gifs
        self.send_games = send_games
        self.send_inline = send_inline
        self.embed_links = embed_links
        self.until_date = until_date

    def to_bytes(self) -> bytes:
        writer = BinaryWriter()
        flags = 0
        flags |= (1 << 0) if self.view_messages else 0
        flags |= (1 << 1) if self.send_messages else 0
        flags |= (1 << 2) if self.send_media else 0
        flags |= (1 << 3) if self.send_stickers else 0
        flags |= (1 << 4) if self.send_gifs else 0
        flags |= (1 << 5) if self.send_games else 0
        flags |= (1 << 6) if self.send_inline else 0
        flags |= (1 << 7) if self.embed_links else 0
        writer.write_int(flags)
        writer.write_int(self.until_date)
        return writer.get_bytes()

    @classmethod
    def from_reader(cls, reader: BinaryReader) -> "ChatBannedRights":
        flags = reader.read_int()
        until_date = reader.read_int()
        return cls(
            view_messages=bool(flags & (1 << 0)),
            send_messages=bool(flags & (1 << 1)),
            send_media=bool(flags & (1 << 2)),
            send_stickers=bool(flags & (1 << 3)),
            send_gifs=bool(flags & (1 << 4)),
            send_games=bool(flags & (1 << 5)),
            send_inline=bool(flags & (1 << 6)),
            embed_links=bool(flags & (1 << 7)),
            until_date=until_date
        )


class ChatPhoto:
    """Represents a chat photo.

    Args:
        photo_id (int): The photo's unique identifier.
        dc_id (int): Data center ID.
    """

    def __init__(self, photo_id: int, dc_id: int):
        self.photo_id = photo_id
        self.dc_id = dc_id

    def to_bytes(self) -> bytes:
        writer = BinaryWriter()
        writer.write_int(0x4757c6f8)  # Constructor ID for chatPhoto
        writer.write_long(self.photo_id)
        writer.write_int(self.dc_id)
        return writer.get_bytes()

    @classmethod
    def from_reader(cls, reader: BinaryReader) -> "ChatPhoto":
        reader.read_int()  # Skip constructor ID
        photo_id = reader.read_long()
        dc_id = reader.read_int()
        return cls(photo_id, dc_id)


class Chat(TLObject):
    """Represents a basic chat object with detailed parameters.

    Args:
        id (int): The chat's unique identifier.
        title (str): The chat's title.
        photo (ChatPhoto, optional): Chat photo.
        participants_count (int): Participant count.
        date (int): Date of creation (Unix timestamp).
        version (int): Chat version.
        creator (bool): Whether the current user is the creator.
        left (bool): Whether the current user has left the group.
        deactivated (bool): Whether the group was migrated.
        call_active (bool): Whether a group call is currently active.
        call_not_empty (bool): Whether there's anyone in the group call.
        noforwards (bool): Whether forwarding messages is disallowed.
        migrated_to (InputChannel, optional): Migrated channel.
        admin_rights (ChatAdminRights, optional): Admin rights of the user.
        default_banned_rights (ChatBannedRights, optional): Default banned rights.
        members (List[User], optional): List of chat members.
    """

    def __init__(self, id: int, title: str, photo: Optional[ChatPhoto], participants_count: int, date: int, version: int,
                 creator: bool = False, left: bool = False, deactivated: bool = False, call_active: bool = False,
                 call_not_empty: bool = False, noforwards: bool = False, migrated_to: Optional[InputChannel] = None,
                 admin_rights: Optional[ChatAdminRights] = None, default_banned_rights: Optional[ChatBannedRights] = None,
                 members: Optional[List[User]] = None):
        super().__init__("chat", 0x6e5afe39)
        self.id = id
        self.title = title
        self.photo = photo
        self.participants_count = participants_count
        self.date = date
        self.version = version
        self.creator = creator
        self.left = left
        self.deactivated = deactivated
        self.call_active = call_active
        self.call_not_empty = call_not_empty
        self.noforwards = noforwards
        self.migrated_to = migrated_to
        self.admin_rights = admin_rights
        self.default_banned_rights = default_banned_rights
        self.members = members or []

    def to_bytes(self) -> bytes:
        writer = BinaryWriter()
        writer.write_int(self.constructor_id)

        flags = 0
        flags |= (1 << 0) if self.creator else 0
        flags |= (1 << 2) if self.left else 0
        flags |= (1 << 5) if self.deactivated else 0
        flags |= (1 << 6) if self.migrated_to else 0
        flags |= (1 << 14) if self.admin_rights else 0
        flags |= (1 << 18) if self.default_banned_rights else 0
        flags |= (1 << 23) if self.call_active else 0
        flags |= (1 << 24) if self.call_not_empty else 0
        flags |= (1 << 25) if self.noforwards else 0
        writer.write_int(flags)

        writer.write_long(self.id)
        writer.write_string(self.title)
        writer.write_obj(self.photo.to_bytes() if self.photo else b"")

        writer.write_int(self.participants_count)
        writer.write_int(self.date)
        writer.write_int(self.version)

        if self.migrated_to:
            writer.write_obj(self.migrated_to.to_bytes())
        if self.admin_rights:
            writer.write_obj(self.admin_rights.to_bytes())
        if self.default_banned_rights:
            writer.write_obj(self.default_banned_rights.to_bytes())

        writer.write_vector(self.members, lambda x: x.to_bytes())
        return writer.get_bytes()

    @classmethod
    def from_reader(cls, reader: BinaryReader) -> "Chat":
        flags = reader.read_int()

        creator = bool(flags & (1 << 0))
        left = bool(flags & (1 << 2))
        deactivated = bool(flags & (1 << 5))
        call_active = bool(flags & (1 << 23))
        call_not_empty = bool(flags & (1 << 24))
        noforwards = bool(flags & (1 << 25))

        id_ = reader.read_long()
        title = reader.read_string()
        photo = ChatPhoto.from_reader(reader) if reader.read_bool() else None
        participants_count = reader.read_int()
        date = reader.read_int()
        version = reader.read_int()

        migrated_to = InputChannel.from_reader(reader) if flags & (1 << 6) else None
        admin_rights = ChatAdminRights.from_reader(reader) if flags & (1 << 14) else None
        default_banned_rights = ChatBannedRights.from_reader(reader) if flags & (1 << 18) else None

        members = reader.read_vector(lambda r: User.from_reader(r))

        return cls(id_, title, photo, participants_count, date, version, creator, left, deactivated, call_active,
                   call_not_empty, noforwards, migrated_to, admin_rights, default_banned_rights, members)