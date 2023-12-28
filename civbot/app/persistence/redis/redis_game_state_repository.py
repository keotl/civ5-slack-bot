import logging
from typing import Optional

from civbot.app.domain.game_state_repository import GameStateRepository
from civbot.app.domain.types import GameState
from civbot.app.persistence.redis.redis_connection import RedisConnection
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject, Override
from jivago.serialization.object_mapper import ObjectMapper


@Component
class RedisGameStateRepository(GameStateRepository):

    @Inject
    def __init__(self, redis: RedisConnection):
        self._redis = redis
        self._object_mapper = ObjectMapper()
        self._logger = logging.getLogger(self.__class__.__name__)

    @Override
    def get_last_known_game_state(self, game_id: str) -> Optional[GameState]:
        saved = self._redis.connection.get(f"gamestate_{game_id}")
        if saved:
            try:
                return self._object_mapper.deserialize(str(saved), GameState)
            except Exception as e:
                self._logger.warning(
                    f"Error while deserializing game state {e}.")
        return None

    @Override
    def set_last_known_game_state(self, game_id: str, state: GameState):
        self._redis.connection.set(f"gamestate_{game_id}",
                                   self._object_mapper.serialize(state))
