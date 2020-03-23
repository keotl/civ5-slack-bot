from jivago.lang.annotations import Inject, Override

from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel
from civbot.app.service.game_state_notifier import GameStateNotifier
from civbot.app.slack.slack_client import SlackClient
from civbot.app.slack.slack_message import SlackMessage
from civbot.app.slack.slack_message_repository import (SavedMessage,
                                                       SlackMessageRepository)
from civbot.app.slack.slack_notification_message_formatter import SlackNotificationMessageFormatter


class SlackStateNotifier(GameStateNotifier):
    """Sends a single message per game turn.
    When the state is updated, the message is updated to match the game state."""

    @Inject
    def __init__(self, message_repository: SlackMessageRepository,
                 message_formatter: SlackNotificationMessageFormatter,
                 slack_client: SlackClient):
        self.message_repository = message_repository
        self.message_formatter = message_formatter
        self.slack_client = slack_client

    @Override
    def notify(self, game_id: str, state: CivHookStateModel):
        existent_message = self.message_repository.find(game_id)
        if existent_message.isPresent() and existent_message.get().turn == state.gameTurn:
            self.slack_client.post_message_or_update(
                SlackMessage(self.message_formatter.format_message(state), existent_message.get().message_ts))
        else:
            message = self.slack_client.post_message_or_update(
                SlackMessage(self.message_formatter.format_message(state)))
            self.message_repository.persist(game_id, SavedMessage(message.ts, state.gameTurn, state))
