from abc import ABC, abstractmethod
from typing import Optional

from civbot.app.service.game_state.types import GameState


class GameStateRepository(ABC):

    @abstractmethod
    def get_last_known_game_state(self, game_id: str) -> Optional[GameState]:
        raise NotImplementedError

    @abstractmethod
    def set_last_known_game_state(self, game_id: str, state: GameState):
        raise NotImplementedError
