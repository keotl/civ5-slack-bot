import logging

from civbot.app.persistence.redis.redis_connection import RedisConnection
from civbot.app.service.turn_notification_message_repository import (
    SavedMessage, TurnNotificationMessageRepository)
from jivago.lang.annotations import Inject, Override
from jivago.lang.nullable import Nullable
from jivago.serialization.object_mapper import ObjectMapper


class RedisTurnNotificationMessageRepository(TurnNotificationMessageRepository
                                             ):

    @Inject
    def __init__(self, redis: RedisConnection):
        self._redis = redis
        self._object_mapper = ObjectMapper()
        self._logger = logging.getLogger(self.__class__.__name__)

    @Override
    def persist(self, game_id: str, message: SavedMessage):
        self._redis.connection.set(f"gamenotification_{game_id}",
                                   self._object_mapper.serialize(message))

    @Override
    def find(self, game_id: str) -> Nullable[SavedMessage]:
        saved = self._redis.connection.get(f"gamenotification_{game_id}")

        if saved:
            try:
                return Nullable(
                    self._object_mapper.deserialize(str(saved), SavedMessage))
            except Exception as e:
                self._logger.warning(
                    f"Error while reading gamenotification. {e}")
        return Nullable.empty()
