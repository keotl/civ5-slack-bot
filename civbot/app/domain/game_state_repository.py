from abc import ABC, abstractmethod
from typing import Dict, Optional

from civbot.app.domain.types import GameState
from civbot.app.service.lock_service import threading
from jivago.lang.annotations import Override


class GameStateRepository(ABC):

    @abstractmethod
    def get_last_known_game_state(self, game_id: str) -> Optional[GameState]:
        raise NotImplementedError

    @abstractmethod
    def set_last_known_game_state(self, game_id: str, state: GameState):
        raise NotImplementedError


class InMemoryGameStateRepository(GameStateRepository):

    def __init__(self):
        self._games: Dict[str, GameState] = {}
        self._lock = threading.Lock()

    @Override
    def get_last_known_game_state(self, game_id: str) -> Optional[GameState]:
        with self._lock:
            return self._games.get(game_id)

    @Override
    def set_last_known_game_state(self, game_id: str, state: GameState):
        with self._lock:
            self._games[game_id] = state
