import threading
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Literal, NamedTuple, Optional

from civbot.app.config.config import Config, Singleton
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject


@dataclass
class GameNotificationConfig(object):
    notifier: Literal["none", "discord", "slack"]
    channel_id: str
    game_notifications_muted_until: datetime
    turn_notifications_muted_until: datetime


@Singleton
@Component
class GameConfigService(object):

    @Inject
    def __init__(self, config: Config):
        self._config = config
        self._lock = threading.Lock()
        self._content: Dict[str, GameNotificationConfig] = {}
        self._game_locks: Dict[str, threading.Lock] = {}
        # TODO - Move to persisted implementation  - keotl 2023-12-27

    def get_game_config(self,
                        game_id: str) -> Optional[GameNotificationConfig]:
        with self._lock:
            if game_id not in self._game_locks:
                self._game_locks[game_id] = threading.Lock()
            lock = self._game_locks[game_id]
        with lock:
            return self._content.get(game_id) or self._default_config()

    def get_game_id_by_channel_id(self, channel_id: str) -> Optional[str]:

        # TODO - Remove this hack when properly supporting connecting a new game  - keotl 2023-12-27
        if channel_id == self._config.default_channel:
            return "ppc"

        for k, v in self._content.items():
            if v.channel_id == channel_id:
                return k

    def _default_config(self):
        return GameNotificationConfig(self._config.notifier,
                                      self._config.default_channel,
                                      datetime.min, datetime.min)

    def save_game_config(self, game_id: str, config: GameNotificationConfig):
        with self._lock:
            if game_id not in self._game_locks:
                self._game_locks[game_id] = threading.Lock()
            lock = self._game_locks[game_id]
        with lock:
            self._content[game_id] = config
