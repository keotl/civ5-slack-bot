from jivago.serialization.object_mapper import ObjectMapper

from civbot.app.resource.civhook.civ_hook_model import (CivHookPlayerModel,
    CivHookStateModel)


SOME_PLAYER: CivHookPlayerModel = ObjectMapper().deserialize("""
{
    "id": 1,
    "nickName": "Atreides",
    "civilization": "Morocco",
    "isTurnComplete": false,
    "isOnline": true,
    "isAlive": true,
    "numWonders": 0,
    "currentEra": 0,
    "enemies": [],
    "allies": []
}""", CivHookPlayerModel)

SOME_GAME_STATE = CivHookStateModel()
SOME_GAME_STATE.gameTurn = 666
SOME_GAME_STATE.players = [SOME_PLAYER]
