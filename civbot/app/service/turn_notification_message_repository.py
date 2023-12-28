from abc import ABC, abstractmethod
from typing import Dict

from jivago.inject.annotation import Component, Singleton
from jivago.lang.annotations import Override
from jivago.lang.nullable import Nullable


class SavedMessage(object):

    def __init__(self, message_ts: str, turn: int):
        self.message_ts = message_ts
        self.turn = turn


class TurnNotificationMessageRepository(ABC):

    @abstractmethod
    def persist(self, game_id: str, message: SavedMessage):
        raise NotImplementedError

    @abstractmethod
    def find(self, game_id: str) -> Nullable[SavedMessage]:
        return NotImplementedError


@Component
@Singleton
class InMemoryTurnNotificationMessageRepository(
        TurnNotificationMessageRepository):
    """Keeps a reference to sent Slack notifications."""

    def __init__(self):
        self.content: Dict[str, SavedMessage] = {}

    @Override
    def persist(self, game_id: str, message: SavedMessage):
        self.content[game_id] = message

    @Override
    def find(self, game_id: str) -> Nullable[SavedMessage]:
        """Returns the message ts."""
        return Nullable(self.content.get(game_id))
