import unittest
from unittest import mock

from jivago.event.async_event_bus import AsyncEventBus

from civbot.app.resource.civhook.civ_hook_resource import CivHookResource
from civbot.app.service.events.game_update_event import GameUpdateEvent
from test.dummy_entities import SOME_GAME_STATE


class testCivHookResource(unittest.TestCase):

    def setUp(self):
        self.async_event_bus_mock: AsyncEventBus = mock.create_autospec(
            AsyncEventBus)
        self.resource = CivHookResource(self.async_event_bus_mock)

    def test_whenTheStateIsUpdated_shouldRaiseEventAndReturn(self):
        self.resource.state_endpoint("game-id", SOME_GAME_STATE)

        self.async_event_bus_mock.emit.assert_called_with(
            GameUpdateEvent("game-id", SOME_GAME_STATE))
