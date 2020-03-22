import requests
from jivago.config.properties.application_properties import (
    ApplicationProperties)
from jivago.lang.annotations import Inject, Override

from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel
from civbot.app.service.game_state_notifier import GameStateNotifier
from civbot.app.slack.slack_message_repository import (SavedMessage,
                                                       SlackMessageRepository)
from civbot.app.slack.slack_notification_message_formatter import SlackNotificationMessageFormatter


class SlackStateNotifier(GameStateNotifier):
    """Sends a single message per game turn.
    When the state is updated, the message is updated to match the game state."""

    @Inject
    def __init__(self, message_repository: SlackMessageRepository,
                 message_formatter: SlackNotificationMessageFormatter,
                 application_properties: ApplicationProperties):
        self.message_repository = message_repository
        self.message_formatter = message_formatter
        self.slack_token = application_properties["slack_token"]
        self.slack_channel = application_properties["slack_channel"]

    @Override
    def notify(self, game_id: str, state: CivHookStateModel):
        existent_message = self.message_repository.find(game_id)

        if existent_message.isPresent() and existent_message.get().turn == state.gameTurn:
            requests.post("https://slack.com/api/chat.update", data={
                "token": self.slack_token,
                "text": self.message_formatter.format_message(state),
                "channel": self.slack_channel,
                "ts": existent_message.get().message_ts})

        else:
            response = requests.post("https://slack.com/api/chat.postMessage", data={
                "token": self.slack_token,
                "channel": self.slack_channel,
                "text": self.message_formatter.format_message(state),
            })
            self.message_repository.persist(game_id, SavedMessage(response.json()["ts"], state.gameTurn))
