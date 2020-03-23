from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject

from civbot.app.slack.slack_message import SlackMessage
from civbot.app.slack.slack_message_repository import SlackMessageRepository, SavedMessage
from civbot.app.slack.slack_notification_message_formatter import SlackNotificationMessageFormatter
from civbot.app.slack.slack_client import SlackClient


@Component
class SlackMessageRefresher(object):
    """Deletes the current turn message, and resends it to provide a new notification."""

    @Inject
    def __init__(self, slack_message_repository: SlackMessageRepository,
                 message_formatter: SlackNotificationMessageFormatter,
                 slack_client: SlackClient):
        self.slack_client = slack_client
        self.slack_message_repository = slack_message_repository
        self.message_formatter = message_formatter

    def refresh_message(self, game_id: str):
        message = self.slack_message_repository.find(game_id)

        if message.isPresent():
            res = self.slack_client.post_message_or_update(
                SlackMessage(self.message_formatter.format_message(message.get().game_state),
                             message.get().message_ts))
            self.slack_message_repository.persist(game_id,
                                                  SavedMessage(res.ts, message.get().turn, message.get().game_state))
