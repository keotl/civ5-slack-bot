import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Literal, Optional

from jivago.lang.annotations import Inject, Override


@dataclass
class GameNotificationConfig(object):
    notifier: Literal["none", "discord", "slack"]
    channel_id: str
    game_notifications_muted_until: datetime
    turn_notifications_muted_until: datetime


def create_default_game_config():
    return GameNotificationConfig("none", "", datetime.min, datetime.min)


class GameConfigService(ABC):

    @abstractmethod
    def get_game_config(self,
                        game_id: str) -> Optional[GameNotificationConfig]:
        raise NotImplementedError

    @abstractmethod
    def get_game_id_by_channel_id(self, channel_id: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def save_game_config(self, game_id: str, config: GameNotificationConfig):
        raise NotImplementedError


class InMemoryGameConfigService(GameConfigService):

    @Inject
    def __init__(self):
        self._lock = threading.Lock()
        self._content: Dict[str, GameNotificationConfig] = {}
        self._game_locks: Dict[str, threading.Lock] = {}

    @Override
    def get_game_config(self,
                        game_id: str) -> Optional[GameNotificationConfig]:
        with self._lock:
            if game_id not in self._game_locks:
                self._game_locks[game_id] = threading.Lock()
            lock = self._game_locks[game_id]
        with lock:
            return self._content.get(game_id) or create_default_game_config()

    @Override
    def get_game_id_by_channel_id(self, channel_id: str) -> Optional[str]:
        for k, v in self._content.items():
            if v.channel_id == channel_id:
                return k

    @Override
    def save_game_config(self, game_id: str, config: GameNotificationConfig):
        with self._lock:
            if game_id not in self._game_locks:
                self._game_locks[game_id] = threading.Lock()
            lock = self._game_locks[game_id]
        with lock:
            self._content[game_id] = config
