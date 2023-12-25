import json
import unittest

from civbot.app.domain.assemble_game_state import assemble_game_state
from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel
from jivago.serialization.object_mapper import ObjectMapper


class AssembleGameStateTests(unittest.TestCase):

    def test_assemble_game_state(self):
        game_state = assemble_game_state(PAYLOAD)

        self.assertEqual(123, game_state.gameTurn)
        self.assertEqual([(0, 1)], game_state.wars, "wars")
        self.assertEqual([(0, 1)], game_state.alliances, "alliances")


json_payload = {
    "gameTurn":
        123,
    "players": [{
        "id": "0",
        "nickName": "keotl",
        "civilization": "Morocco",
        "isTurnComplete": True,
        "isOnline": True,
        "isAlive": True,
        "numWonders": 0,
        "currentEra": 0,
        "enemies": ["1"],
        "allies": ["doctor"],
    }, {
        "id": "1",
        "nickName": "doctor",
        "civilization": "Gallifreyan",
        "isTurnComplete": True,
        "isOnline": True,
        "isAlive": True,
        "numWonders": 0,
        "currentEra": 0,
        "enemies": ["0"],
        "allies": ["keotl"],
    }]
}

PAYLOAD = ObjectMapper().deserialize(json.dumps(json_payload),
                                     CivHookStateModel)
