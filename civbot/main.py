import os

from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.jivago_application import JivagoApplication

import civbot.app
from civbot.app.discord.discord_game_notifier import DiscordGameNotifier
from civbot.app.service.game_state_notifier import GameStateNotifier
from civbot.app.slack.slack_state_notifier import SlackStateNotifier


class SlackContext(ProductionJivagoContext):

    def configure_service_locator(self):
        super().configure_service_locator()
        if os.environ.get("NOTIFIER") in ("slack", None):
            self.service_locator().bind(GameStateNotifier, SlackStateNotifier)
        if os.environ.get("NOTIFIER") == "discord":
            self.service_locator().bind(GameStateNotifier, DiscordGameNotifier)


application = JivagoApplication(civbot.app, context=SlackContext)

if __name__ == '__main__':
    application.run_dev(host="0.0.0.0", port=4000)
