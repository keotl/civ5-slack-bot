from jivago.lang.annotations import Override

from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel
from civbot.app.service.game_state_notifier import GameStateNotifier
from civbot.app.slack.slack_message_repository import SlackMessageRepository


class SlackStateNotifier(GameStateNotifier):
    """Sends a single message per game turn.
    When the state is updated, the message is updated to match the game state."""

    def __init__(self, message_repository: SlackMessageRepository):
        self.message_repository = message_repository

    @Override
    def notify(self, game_id: str, state: CivHookStateModel):
        pass
