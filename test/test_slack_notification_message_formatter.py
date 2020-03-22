import unittest
from unittest import mock

from civbot.app.slack.slack_notification_message_formatter import (
    SlackNotificationMessageFormatter)
from test.dummy_entities import SOME_GAME_STATE, SOME_PLAYER


class SlackNotificationMessageFormatterTests(unittest.TestCase):

    def setUp(self):
        self.formatter = SlackNotificationMessageFormatter()

    def test_shows_remaining_players(self):
        message = self.formatter.format_message(SOME_GAME_STATE)

        self.assertTrue(f"{SOME_PLAYER.nickName}" in message)

    def test_shows_turn_number(self):
        message = self.formatter.format_message(SOME_GAME_STATE)

        self.assertTrue(str(SOME_GAME_STATE.gameTurn) in message)
