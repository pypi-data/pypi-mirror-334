from typing import Optional, List
from neongram.parser.tl_object import TLObject
from neongram.utils.binary_reader import BinaryReader
from neongram.utils.binary_writer import BinaryWriter
from neongram.types.chat import ChatAdminRights, ChatBannedRights, ChatPhoto


class RestrictionReason:
    """Represents a restriction reason for a channel.

    Args:
        reason (str): The restriction reason (e.g., "spam").
        text (str): Description of the restriction.
    """

    def __init__(self, reason: str, text: str):
        self.reason = reason
        self.text = text

    def to_bytes(self) -> bytes:
        writer = BinaryWriter()
        writer.write_int(0xeedd3ad6)  # Constructor ID for restrictionReason
        writer.write_string(self.reason)
        writer.write_string(self.text)
        return writer.get_bytes()

    @classmethod
    def from_reader(cls, reader: BinaryReader) -> "RestrictionReason":
        reader.read_int()  # Skip constructor ID
        reason = reader.read_string()
        text = reader.read_string()
        return cls(reason, text)


class Username:
    """Represents a username for a channel.

    Args:
        username (str): The username.
        active (bool): Whether the username is active.
    """

    def __init__(self, username: str, active: bool = True):
        self.username = username
        self.active = active

    def to_bytes(self) -> bytes:
        writer = BinaryWriter()
        writer.write_int(0x35196b3a)  # Constructor ID for Username
        flags = 0
        flags |= (1 << 0) if self.active else 0
        writer.write_int(flags)
        writer.write_string(self.username)
        return writer.get_bytes()

    @classmethod
    def from_reader(cls, reader: BinaryReader) -> "Username":
        reader.read_int()  # Skip constructor ID
        flags = reader.read_int()
        active = bool(flags & (1 << 0))
        username = reader.read_string()
        return cls(username, active)


class PeerColor:
    """Represents a peer color for a channel.

    Args:
        color_id (int): The color ID.
    """

    def __init__(self, color_id: int):
        self.color_id = color_id

    def to_bytes(self) -> bytes:
        writer = BinaryWriter()
        writer.write_int(0x8a75e65e)  # Constructor ID for peerColor
        writer.write_int(self.color_id)
        return writer.get_bytes()

    @classmethod
    def from_reader(cls, reader: BinaryReader) -> "PeerColor":
        reader.read_int()  # Skip constructor ID
        color_id = reader.read_int()
        return cls(color_id)


class EmojiStatus:
    """Represents an emoji status for a channel.

    Args:
        emoji_id (int): The emoji ID.
    """

    def __init__(self, emoji_id: int):
        self.emoji_id = emoji_id

    def to_bytes(self) -> bytes:
        writer = BinaryWriter()
        writer.write_int(0x2de11aae)  # Constructor ID for emojiStatus
        writer.write_long(self.emoji_id)
        return writer.get_bytes()

    @classmethod
    def from_reader(cls, reader: BinaryReader) -> "EmojiStatus":
        reader.read_int()  # Skip constructor ID
        emoji_id = reader.read_long()
        return cls(emoji_id)


class Channel(TLObject):
    """Represents a channel or supergroup with detailed parameters.

    Args:
        id (int): The channel's unique identifier.
        access_hash (int, optional): Access hash for the channel.
        title (str): The channel's title.
        username (str, optional): Main active username.
        photo (ChatPhoto, optional): Profile photo.
        date (int): Date of joining or creation (Unix timestamp).
        creator (bool): Whether the current user is the creator.
        left (bool): Whether the current user has left.
        broadcast (bool): Whether this is a channel.
        verified (bool): Whether the channel is verified.
        megagroup (bool): Whether this is a supergroup.
        restricted (bool): Whether the channel is restricted.
        signatures (bool): Whether signatures are enabled.
        min (bool): Whether this is a min channel.
        scam (bool): Whether the channel is marked as a scam.
        has_link (bool): Whether the channel has a linked discussion group.
        has_geo (bool): Whether the channel has a geoposition.
        slowmode_enabled (bool): Whether slow mode is enabled.
        call_active (bool): Whether a group call or livestream is active.
        call_not_empty (bool): Whether the call or livestream has participants.
        fake (bool): Whether the channel is marked as fake.
        gigagroup (bool): Whether this is a gigagroup.
        noforwards (bool): Whether forwarding is disallowed.
        join_to_send (bool): Whether users must join to send messages.
        join_request (bool): Whether join requests need approval.
        forum (bool): Whether the supergroup is a forum.
        stories_hidden (bool): Whether stories are hidden.
        stories_hidden_min (bool): Whether stories_hidden is reliable.
        stories_unavailable (bool): Whether stories are unavailable.
        signature_profiles (bool): Whether admin messages link to profiles.
        restriction_reason (List[RestrictionReason], optional): Restriction reasons.
        admin_rights (ChatAdminRights, optional): Admin rights of the user.
        banned_rights (ChatBannedRights, optional): Banned rights of the user.
        default_banned_rights (ChatBannedRights, optional): Default banned rights.
        participants_count (int, optional): Participant count.
        usernames (List[Username], optional): Additional usernames.
        stories_max_id (int, optional): Maximum read story ID.
        color (PeerColor, optional): Accent color.
        profile_color (PeerColor, optional): Profile color.
        emoji_status (EmojiStatus, optional): Emoji status.
        level (int, optional): Boost level.
        subscription_until_date (int, optional): Telegram Star subscription expiration.
    """

    def __init__(self, id: int, title: str, date: int, creator: bool = False, left: bool = False, broadcast: bool = False,
                 verified: bool = False, megagroup: bool = False, restricted: bool = False, signatures: bool = False,
                 min: bool = False, scam: bool = False, has_link: bool = False, has_geo: bool = False,
                 slowmode_enabled: bool = False, call_active: bool = False, call_not_empty: bool = False,
                 fake: bool = False, gigagroup: bool = False, noforwards: bool = False, join_to_send: bool = False,
                 join_request: bool = False, forum: bool = False, stories_hidden: bool = False,
                 stories_hidden_min: bool = False, stories_unavailable: bool = False, signature_profiles: bool = False,
                 access_hash: Optional[int] = None, username: Optional[str] = None, photo: Optional[ChatPhoto] = None,
                 restriction_reason: Optional[List[RestrictionReason]] = None, admin_rights: Optional[ChatAdminRights] = None,
                 banned_rights: Optional[ChatBannedRights] = None, default_banned_rights: Optional[ChatBannedRights] = None,
                 participants_count: Optional[int] = None, usernames: Optional[List[Username]] = None,
                 stories_max_id: Optional[int] = None, color: Optional[PeerColor] = None,
                 profile_color: Optional[PeerColor] = None, emoji_status: Optional[EmojiStatus] = None,
                 level: Optional[int] = None, subscription_until_date: Optional[int] = None):
        super().__init__("channel", 0x3d5f567c)
        self.id = id
        self.access_hash = access_hash
        self.title = title
        self.username = username
        self.photo = photo
        self.date = date
        self.creator = creator
        self.left = left
        self.broadcast = broadcast
        self.verified = verified
        self.megagroup = megagroup
        self.restricted = restricted
        self.signatures = signatures
        self.min = min
        self.scam = scam
        self.has_link = has_link
        self.has_geo = has_geo
        self.slowmode_enabled = slowmode_enabled
        self.call_active = call_active
        self.call_not_empty = call_not_empty
        self.fake = fake
        self.gigagroup = gigagroup
        self.noforwards = noforwards
        self.join_to_send = join_to_send
        self.join_request = join_request
        self.forum = forum
        self.stories_hidden = stories_hidden
        self.stories_hidden_min = stories_hidden_min
        self.stories_unavailable = stories_unavailable
        self.signature_profiles = signature_profiles
        self.restriction_reason = restriction_reason or []
        self.admin_rights = admin_rights
        self.banned_rights = banned_rights
        self.default_banned_rights = default_banned_rights
        self.participants_count = participants_count
        self.usernames = usernames or []
        self.stories_max_id = stories_max_id
        self.color = color
        self.profile_color = profile_color
        self.emoji_status = emoji_status
        self.level = level
        self.subscription_until_date = subscription_until_date

    def to_bytes(self) -> bytes:
        writer = BinaryWriter()
        writer.write_int(self.constructor_id)

        flags = 0
        flags |= (1 << 0) if self.creator else 0
        flags |= (1 << 2) if self.left else 0
        flags |= (1 << 5) if self.broadcast else 0
        flags |= (1 << 7) if self.verified else 0
        flags |= (1 << 8) if self.megagroup else 0
        flags |= (1 << 9) if self.restricted else 0
        flags |= (1 << 11) if self.signatures else 0
        flags |= (1 << 12) if self.min else 0
        flags |= (1 << 19) if self.scam else 0
        flags |= (1 << 20) if self.has_link else 0
        flags |= (1 << 21) if self.has_geo else 0
        flags |= (1 << 22) if self.slowmode_enabled else 0
        flags |= (1 << 23) if self.call_active else 0
        flags |= (1 << 24) if self.call_not_empty else 0
        flags |= (1 << 25) if self.fake else 0
        flags |= (1 << 26) if self.gigagroup else 0
        flags |= (1 << 27) if self.noforwards else 0
        flags |= (1 << 28) if self.join_to_send else 0
        flags |= (1 << 29) if self.join_request else 0
        flags |= (1 << 30) if self.forum else 0
        flags |= (1 << 6) if self.username else 0
        flags |= (1 << 9) if self.restriction_reason else 0
        flags |= (1 << 13) if self.access_hash else 0
        flags |= (1 << 14) if self.admin_rights else 0
        flags |= (1 << 15) if self.banned_rights else 0
        flags |= (1 << 18) if self.default_banned_rights else 0
        flags |= (1 << 17) if self.participants_count is not None else 0
        writer.write_int(flags)

        flags2 = 0
        flags2 |= (1 << 0) if self.usernames else 0
        flags2 |= (1 << 1) if self.stories_hidden else 0
        flags2 |= (1 << 2) if self.stories_hidden_min else 0
        flags2 |= (1 << 3) if self.stories_unavailable else 0
        flags2 |= (1 << 4) if self.stories_max_id is not None else 0
        flags2 |= (1 << 7) if self.color else 0
        flags2 |= (1 << 8) if self.profile_color else 0
        flags2 |= (1 << 9) if self.emoji_status else 0
        flags2 |= (1 << 10) if self.level is not None else 0
        flags2 |= (1 << 11) if self.subscription_until_date is not None else 0
        flags2 |= (1 << 12) if self.signature_profiles else 0
        writer.write_int(flags2)

        writer.write_long(self.id)
        if self.access_hash is not None:
            writer.write_long(self.access_hash)
        writer.write_string(self.title)
        if self.username:
            writer.write_string(self.username)
        writer.write_obj(self.photo.to_bytes() if self.photo else b"")
        writer.write_int(self.date)
        if self.restriction_reason:
            writer.write_vector(self.restriction_reason, lambda x: writer.write_obj(x.to_bytes()))
        if self.admin_rights:
            writer.write_obj(self.admin_rights.to_bytes())
        if self.banned_rights:
            writer.write_obj(self.banned_rights.to_bytes())
        if self.default_banned_rights:
            writer.write_obj(self.default_banned_rights.to_bytes())
        if self.participants_count is not None:
            writer.write_int(self.participants_count)
        if self.usernames:
            writer.write_vector(self.usernames, lambda x: writer.write_obj(x.to_bytes()))
        if self.stories_max_id is not None:
            writer.write_int(self.stories_max_id)
        if self.color:
            writer.write_obj(self.color.to_bytes())
        if self.profile_color:
            writer.write_obj(self.profile_color.to_bytes())
        if self.emoji_status:
            writer.write_obj(self.emoji_status.to_bytes())
        if self.level is not None:
            writer.write_int(self.level)
        if self.subscription_until_date is not None:
            writer.write_int(self.subscription_until_date)
        return writer.get_bytes()

    @classmethod
    def from_reader(cls, reader: BinaryReader) -> "Channel":
        flags = reader.read_int()
        flags2 = reader.read_int()

        creator = bool(flags & (1 << 0))
        left = bool(flags & (1 << 2))
        broadcast = bool(flags & (1 << 5))
        verified = bool(flags & (1 << 7))
        megagroup = bool(flags & (1 << 8))
        restricted = bool(flags & (1 << 9))
        signatures = bool(flags & (1 << 11))
        min = bool(flags & (1 << 12))
        scam = bool(flags & (1 << 19))
        has_link = bool(flags & (1 << 20))
        has_geo = bool(flags & (1 << 21))
        slowmode_enabled = bool(flags & (1 << 22))
        call_active = bool(flags & (1 << 23))
        call_not_empty = bool(flags & (1 << 24))
        fake = bool(flags & (1 << 25))
        gigagroup = bool(flags & (1 << 26))
        noforwards = bool(flags & (1 << 27))
        join_to_send = bool(flags & (1 << 28))
        join_request = bool(flags & (1 << 29))
        forum = bool(flags & (1 << 30))
        stories_hidden = bool(flags2 & (1 << 1))
        stories_hidden_min = bool(flags2 & (1 << 2))
        stories_unavailable = bool(flags2 & (1 << 3))
        signature_profiles = bool(flags2 & (1 << 12))

        id_ = reader.read_long()
        access_hash = reader.read_long() if flags & (1 << 13) else None
        title = reader.read_string()
        username = reader.read_string() if flags & (1 << 6) else None
        photo = ChatPhoto.from_reader(reader) if reader.read_bool() else None
        date = reader.read_int()
        restriction_reason = reader.read_vector(lambda r: RestrictionReason.from_reader(r)) if flags & (1 << 9) else None
        admin_rights = ChatAdminRights.from_reader(reader) if flags & (1 << 14) else None
        banned_rights = ChatBannedRights.from_reader(reader) if flags & (1 << 15) else None
        default_banned_rights = ChatBannedRights.from_reader(reader) if flags & (1 << 18) else None
        participants_count = reader.read_int() if flags & (1 << 17) else None
        usernames = reader.read_vector(lambda r: Username.from_reader(r)) if flags2 & (1 << 0) else None
        stories_max_id = reader.read_int() if flags2 & (1 << 4) else None
        color = PeerColor.from_reader(reader) if flags2 & (1 << 7) else None
        profile_color = PeerColor.from_reader(reader) if flags2 & (1 << 8) else None
        emoji_status = EmojiStatus.from_reader(reader) if flags2 & (1 << 9) else None
        level = reader.read_int() if flags2 & (1 << 10) else None
        subscription_until_date = reader.read_int() if flags2 & (1 << 11) else None

        return cls(
            id_, title, date, creator, left, broadcast, verified, megagroup, restricted, signatures, min, scam,
            has_link, has_geo, slowmode_enabled, call_active, call_not_empty, fake, gigagroup, noforwards,
            join_to_send, join_request, forum, stories_hidden, stories_hidden_min, stories_unavailable,
            signature_profiles, access_hash, username, photo, restriction_reason, admin_rights, banned_rights,
            default_banned_rights, participants_count, usernames, stories_max_id, color, profile_color,
            emoji_status, level, subscription_until_date
        )