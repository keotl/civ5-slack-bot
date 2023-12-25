import os

from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.jivago_application import JivagoApplication

import civbot.app
from civbot.app.discord.discord_event_notifier import DiscordEventNotifier
from civbot.app.discord.discord_turn_notifier import DiscordTurnNotifier
from civbot.app.domain.game_state_repository import (
    GameStateRepository, InMemoryGameStateRepository)
from civbot.app.service.game_event_notifier import (GameEventNotifier,
                                                    NoopGameEventNotifier)
from civbot.app.service.turn_notifier import TurnNotifier
from civbot.app.slack.slack_turn_notifier import SlackTurnNotifier


class Context(ProductionJivagoContext):

    def configure_service_locator(self):
        super().configure_service_locator()
        self.service_locator().bind(GameStateRepository,
                                    InMemoryGameStateRepository())

        if os.environ.get("NOTIFIER") in ("slack", None):
            self.service_locator().bind(TurnNotifier, SlackTurnNotifier)
            self.service_locator().bind(GameEventNotifier,
                                        NoopGameEventNotifier)
        if os.environ.get("NOTIFIER") == "discord":
            self.service_locator().bind(TurnNotifier, DiscordTurnNotifier)
            self.service_locator().bind(GameEventNotifier,
                                        DiscordEventNotifier)


application = JivagoApplication(civbot.app, context=Context)

if __name__ == '__main__':
    application.run_dev(host="0.0.0.0", port=4000)
