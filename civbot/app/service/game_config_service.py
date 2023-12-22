from typing import Literal, NamedTuple, Optional

from civbot.app.config.config import Config
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject


class GameNotificationConfig(NamedTuple):
    notifier: Literal["none", "discord", "slack"]
    channel_id: str


@Component
class GameConfigService(object):

    @Inject
    def __init__(self, config: Config):
        self._config = config

    def get_game_config(self,
                        game_id: str) -> Optional[GameNotificationConfig]:
        # TODO - Allow config per game instead of global  - keotl 2023-12-22
        return GameNotificationConfig(self._config.notifier,
                                      self._config.default_channel)
