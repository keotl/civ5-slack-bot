import unittest

from civbot.app.domain.game_events import WarEndedEvent, WarStartedEvent
from civbot.app.domain.game_state_diff import compute_game_state_diff
from civbot.app.domain.types import GameState, PlayerState


class GameStateDiffTests(unittest.TestCase):

    def test_generate_war_started_events(self):
        events = compute_game_state_diff(
            GameState(123, [_player(0), _player(1)], [], []),
            GameState(123, [_player(0), _player(1)], [(0, 1)], []))

        self.assertEqual(1, len(events))
        self.assertIsInstance(events[0], WarStartedEvent)

    def test_generate_war_ended_events(self):
        events = compute_game_state_diff(
            GameState(123, [_player(0), _player(1)], [(0, 1)], []),
            GameState(123, [_player(0), _player(1)], [], []))

        self.assertEqual(1, len(events))
        self.assertIsInstance(events[0], WarEndedEvent)


def _player(id: int) -> PlayerState:
    return PlayerState(id, str(id), str(id), 0, 0)
