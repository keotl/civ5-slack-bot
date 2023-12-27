from typing import List

from civbot.app.discord.discord_client import DiscordClient
from civbot.app.domain.types import GameEvent
from civbot.app.service.game_config_service import GameConfigService
from civbot.app.service.game_event_notifier import GameEventNotifier
from civbot.app.util.clock import Clock
from jivago.lang.annotations import Inject, Override


class DiscordEventNotifier(GameEventNotifier):

    @Inject
    def __init__(self, discord: DiscordClient,
                 game_config_service: GameConfigService, clock: Clock):
        self._discord = discord
        self._config_service = game_config_service
        self._clock = clock

    @Override
    def notify(self, game_id: str, events: List[GameEvent]):
        config = self._config_service.get_game_config(game_id)
        if (config is None or config.notifier != "discord"
                or config.game_notifications_muted_until > self._clock.now()):
            return

        for event in events:
            self._discord.create_message(config.channel_id,
                                         event.notification_message()["text"])
