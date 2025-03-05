from dataclasses import asdict
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any

@dataclass
class EmbedFooter:
    text: str
    icon_url: Optional[str] = None

    def to_dict(self):
        return asdict(self)

@dataclass
class EmbedImage:
    url: str

    def to_dict(self):
        return asdict(self)

@dataclass
class EmbedThumbnail:
    url: str

    def to_dict(self):
        return asdict(self)

@dataclass
class EmbedVideo:
    url: str

    def to_dict(self):
        return asdict(self)

@dataclass
class EmbedProvider:
    name: str
    url: Optional[str] = None

    def to_dict(self):
        return asdict(self)

@dataclass
class EmbedAuthor:
    name: str
    url: Optional[str] = None
    icon_url: Optional[str] = None

    def to_dict(self):
        return asdict(self)

@dataclass
class EmbedField:
    name: str
    value: str
    inline: Optional[bool] = False

    def to_dict(self):
        return asdict(self)

@dataclass
class Embed:
    title: Optional[str] = None
    type: Optional[str] = "rich"
    description: Optional[str] = None
    url: Optional[str] = None
    timestamp: Optional[datetime] = None
    color: Optional[int] = None
    footer: Optional[EmbedFooter] = None
    image: Optional[EmbedImage] = None
    thumbnail: Optional[EmbedThumbnail] = None
    video: Optional[EmbedVideo] = None
    provider: Optional[EmbedProvider] = None
    author: Optional[EmbedAuthor] = None
    fields: Optional[List[EmbedField]] = field(default_factory=list)

    def to_dict(self):
        embed_dict = asdict(self)
        # Convert nested objects to dictionaries
        if self.footer:
            embed_dict['footer'] = self.footer.to_dict()
        if self.image:
            embed_dict['image'] = self.image.to_dict()
        if self.thumbnail:
            embed_dict['thumbnail'] = self.thumbnail.to_dict()
        if self.video:
            embed_dict['video'] = self.video.to_dict()
        if self.provider:
            embed_dict['provider'] = self.provider.to_dict()
        if self.author:
            embed_dict['author'] = self.author.to_dict()
        if self.fields:
            embed_dict['fields'] = [field.to_dict() for field in self.fields]
        return embed_dict

@dataclass
class AllowedMentions:
    parse: Optional[List[str]] = None
    roles: Optional[List[str]] = None
    users: Optional[List[str]] = None
    replied_user: Optional[bool] = None

    def to_dict(self):
        return asdict(self)

@dataclass
class MessageComponent:
    type: int
    components: List[Dict[str, Any]]

    def to_dict(self):
        return asdict(self)

@dataclass
class PartialAttachment:
    id: str
    filename: str
    description: Optional[str] = None

    def to_dict(self):
        return asdict(self)

@dataclass
class PollRequest:
    question: str
    options: List[str]

    def to_dict(self):
        return asdict(self)

@dataclass
class WebhookMessage:
    content: Optional[str] = None
    username: Optional[str] = "opencve"
    avatar_url: Optional[str] = None
    tts: Optional[bool] = False
    embeds: Optional[List[Embed]] = field(default_factory=list)
    allowed_mentions: Optional[AllowedMentions] = None
    components: Optional[List[MessageComponent]] = field(default_factory=list)
    files: Optional[List[bytes]] = field(default_factory=list)
    payload_json: Optional[str] = None
    attachments: Optional[List[PartialAttachment]] = field(default_factory=list)
    flags: Optional[int] = None
    thread_name: Optional[str] = None
    applied_tags: Optional[List[str]] = field(default_factory=list)
    poll: Optional[PollRequest] = None

    def to_dict(self):
        message_dict = asdict(self)
        # Convert nested objects to dictionaries
        if self.allowed_mentions:
            message_dict['allowed_mentions'] = self.allowed_mentions.to_dict()
        if self.components:
            message_dict['components'] = [component.to_dict() for component in self.components]
        if self.attachments:
            message_dict['attachments'] = [attachment.to_dict() for attachment in self.attachments]
        if self.poll:
            message_dict['poll'] = self.poll.to_dict()
        if self.embeds:
            message_dict['embeds'] = [embed.to_dict() for embed in self.embeds]
        return message_dict
