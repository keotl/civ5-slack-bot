from jivago.config.production_jivago_context import ProductionJivagoContext
from jivago.jivago_application import JivagoApplication

import civbot.app
from civbot.app.service.game_state_notifier import GameStateNotifier
from civbot.app.slack.slack_state_notifier import SlackStateNotifier


class SlackContext(ProductionJivagoContext):

    def configure_service_locator(self):
        super().configure_service_locator()
        self.service_locator().bind(GameStateNotifier, SlackStateNotifier)


application = JivagoApplication(civbot.app, context=SlackContext)

if __name__ == '__main__':
    application.run_dev(host="0.0.0.0", port=4000)
