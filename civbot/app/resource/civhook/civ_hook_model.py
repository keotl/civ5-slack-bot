from typing import List

from jivago.lang.annotations import Serializable


@Serializable
class CivHookPlayerModel(object):
    id: int
    nickName: str
    civilization: str
    isTurnComplete: bool
    isOnline: bool
    isAlive: bool


@Serializable
class CivHookStateModel(object):
    gameTurn: int
    players: List[CivHookPlayerModel]
