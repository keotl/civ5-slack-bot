from abc import ABC, abstractmethod
from typing import List

from civbot.app.domain.types import GameEvent


class GameEventNotifier(ABC):

    @abstractmethod
    def notify(self, game_id: str, events: List[GameEvent]):
        raise NotImplementedError


class NoopGameEventNotifier(GameEventNotifier):

    def notify(self, game_id: str, events: List[GameEvent]):
        pass
