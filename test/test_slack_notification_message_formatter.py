import unittest
from test.utils.dummy_entities import SOME_GAME_STATE, SOME_PLAYER

from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel
from civbot.app.slack.slack_notification_message_formatter import \
    SlackNotificationMessageFormatter
from jivago.serialization.object_mapper import ObjectMapper


class SlackNotificationMessageFormatterTests(unittest.TestCase):

    def setUp(self):
        self.formatter = SlackNotificationMessageFormatter()

    def test_shows_remaining_players(self):
        message = self.formatter.format_message(SOME_GAME_STATE)

        self.assertTrue(f"{SOME_PLAYER.nickName}" in message)

    def test_hides_players_whose_turn_has_ended(self):
        state = clone(SOME_GAME_STATE)
        state.players[0].isTurnComplete = True

        message = self.formatter.format_message(state)

        self.assertFalse(f"{SOME_PLAYER.nickName}" in message)

    def test_shows_turn_number(self):
        message = self.formatter.format_message(SOME_GAME_STATE)

        self.assertTrue(str(SOME_GAME_STATE.gameTurn) in message)


def clone(state: CivHookStateModel) -> CivHookStateModel:
    object_mapper = ObjectMapper()
    return object_mapper.deserialize(object_mapper.serialize(state),
                                     CivHookStateModel)
