from abc import ABC, abstractmethod
from typing import List, NamedTuple, Tuple, TypedDict


class PlayerState(NamedTuple):
    id: int
    nickName: str
    civilization: str
    currentEra: int
    numWonders: int


class GameState(NamedTuple):
    gameTurn: int
    players: List[PlayerState]
    wars: List[Tuple[int, int]]
    alliances: List[Tuple[int, int]]


class NotificationMessage(TypedDict):
    text: str


class GameEvent(ABC):

    @abstractmethod
    def notification_message(self) -> NotificationMessage:
        raise NotImplementedError
