from typing import List, Optional

from jivago.lang.annotations import Serializable


@Serializable
class CivHookPlayerModel(object):
    id: int
    nickName: str
    civilization: str
    isHuman: bool
    isTurnComplete: bool
    isTurnActive: bool
    isOnline: bool
    isAlive: bool
    numWonders: int
    currentEra: int
    enemies: List[str]
    allies: List[str]


@Serializable
class CivHookGameStateModel(object):
    winner: int
    victoryType: int


@Serializable
class CivHookStateModel(object):
    gameTurn: int
    players: List[CivHookPlayerModel]
    game: CivHookGameStateModel
