import logging
import os

from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.jivago_application import JivagoApplication

import civbot.app
from civbot.app.discord.discord_event_notifier import DiscordEventNotifier
from civbot.app.discord.discord_turn_notifier import DiscordTurnNotifier
from civbot.app.domain.game_state_repository import (
    GameStateRepository, InMemoryGameStateRepository)
from civbot.app.persistence.redis.redis_game_config_service import \
    RedisGameConfigService
from civbot.app.persistence.redis.redis_game_state_repository import \
    RedisGameStateRepository
from civbot.app.persistence.redis.redis_lock_service import RedisLockService
from civbot.app.persistence.redis.redis_turn_notification_message_repository import \
    RedisTurnNotificationMessageRepository
from civbot.app.service.game_config_service import (GameConfigService,
                                                    InMemoryGameConfigService)
from civbot.app.service.game_event_notifier import (GameEventNotifier,
                                                    NoopGameEventNotifier)
from civbot.app.service.lock_service import InMemoryLockService, LockService
from civbot.app.service.turn_notification_message_repository import (
    InMemoryTurnNotificationMessageRepository,
    TurnNotificationMessageRepository)
from civbot.app.service.turn_notifier import TurnNotifier
from civbot.app.slack.slack_turn_notifier import SlackTurnNotifier

logging.getLogger().setLevel(logging.INFO)


class Context(ProductionJivagoContext):

    def configure_service_locator(self):
        super().configure_service_locator()
        if os.environ.get("NOTIFIER") in ("slack", None):
            self.service_locator().bind(TurnNotifier, SlackTurnNotifier)
            self.service_locator().bind(GameEventNotifier,
                                        NoopGameEventNotifier)
        if os.environ.get("NOTIFIER") == "discord":
            self.service_locator().bind(TurnNotifier, DiscordTurnNotifier)
            self.service_locator().bind(GameEventNotifier,
                                        DiscordEventNotifier)

        if os.environ.get("PERSISTENCE_PROVIDER") == "none":
            self.service_locator().bind(GameStateRepository,
                                        InMemoryGameStateRepository())
            self.service_locator().bind(LockService, InMemoryLockService())
            self.service_locator().bind(GameConfigService,
                                        InMemoryGameConfigService())
            self.service_locator().bind(
                TurnNotificationMessageRepository,
                InMemoryTurnNotificationMessageRepository())

        elif os.environ.get("PERSISTENCE_PROVIDER") == "redis":
            self.service_locator().bind(GameStateRepository,
                                        RedisGameStateRepository)
            self.service_locator().bind(LockService, RedisLockService)
            self.service_locator().bind(GameConfigService,
                                        RedisGameConfigService)
            self.service_locator().bind(
                TurnNotificationMessageRepository,
                RedisTurnNotificationMessageRepository)


application = JivagoApplication(civbot.app, context=Context)

if __name__ == '__main__':
    application.run_dev(host="0.0.0.0", port=4000)
