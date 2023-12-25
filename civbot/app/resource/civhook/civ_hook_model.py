from typing import List

from jivago.lang.annotations import Serializable


@Serializable
class CivHookPlayerModel(object):
    id: int
    nickName: str
    civilization: str
    isHuman: bool
    isTurnComplete: bool
    isOnline: bool
    isAlive: bool
    numWonders: int
    currentEra: int
    enemies: List[str]
    allies: List[str]


@Serializable
class CivHookStateModel(object):
    gameTurn: int
    players: List[CivHookPlayerModel]

