from typing import TypedDict


class DiscordMessage(TypedDict):
    id: str
    content: str
    channel_id: str

