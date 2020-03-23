import unittest
from unittest import mock

from jivago.lang.nullable import Nullable

from civbot.app.slack.slack_client import SlackClient
from civbot.app.slack.slack_message import SlackMessage
from civbot.app.slack.slack_message_refresher import SlackMessageRefresher
from civbot.app.slack.slack_message_repository import (SavedMessage,
                                                       SlackMessageRepository)
from civbot.app.slack.slack_notification_message_formatter import (
    SlackNotificationMessageFormatter)
from test.utils.dummy_entities import SOME_GAME_STATE


class SlackMessageRefresherTests(unittest.TestCase):

    def setUp(self):
        self.message_repository_mock: SlackMessageRepository = mock.create_autospec(SlackMessageRepository)
        self.message_formatter_mock: SlackNotificationMessageFormatter = mock.create_autospec(
            SlackNotificationMessageFormatter)
        self.slack_client_mock: SlackClient = mock.create_autospec(SlackClient)
        self.message_refresher = SlackMessageRefresher(self.message_repository_mock, self.message_formatter_mock,
                                                       self.slack_client_mock)

        self.message_formatter_mock.format_message.return_value = "formatted-message"

    def test_sends_a_notification_if_one_has_already_been_sent(self):
        self.message_repository_mock.find.return_value = Nullable(SavedMessage("ts", 666, SOME_GAME_STATE))

        self.message_refresher.refresh_message("game-id")

        self.slack_client_mock.post_message_or_update.assert_called_with(SlackMessage("formatted-message", "ts"))

    def test_saves_the_updated_message_ts(self):
        self.message_repository_mock.find.return_value = Nullable(SavedMessage("ts", 666, SOME_GAME_STATE))

        self.message_refresher.refresh_message("game-id")

        self.message_repository_mock.persist.assert_called()
