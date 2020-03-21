import unittest
from unittest import mock

from civbot.app.service.events.game_update_event import GameUpdateEvent
from civbot.app.service.game_state_notifier import (GameStateNotifier,
    NotificationWorker)
from test.dummy_entities import SOME_GAME_STATE


class NotificationWorkerTests(unittest.TestCase):

    def setUp(self):
        self.notifier_mock: GameStateNotifier = mock.create_autospec(GameStateNotifier)
        self.worker = NotificationWorker(self.notifier_mock)

    def test_whenHandlingEvent_thenNotifierIsInvoked(self):
        self.worker.handle(GameUpdateEvent("game-id", SOME_GAME_STATE))

        self.notifier_mock.notify.assert_called_with("game-id", SOME_GAME_STATE)
