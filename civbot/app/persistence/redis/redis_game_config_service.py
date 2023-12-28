import logging
from typing import Optional

from civbot.app.persistence.redis.redis_connection import RedisConnection
from civbot.app.service.game_config_service import (GameConfigService,
                                                    GameNotificationConfig,
                                                    create_default_game_config)
from jivago.lang.annotations import Inject, Override
from jivago.serialization.object_mapper import ObjectMapper


class RedisGameConfigService(GameConfigService):

    @Inject
    def __init__(self, redis: RedisConnection):
        self._redis = redis
        self._object_mapper = ObjectMapper()
        self._logger = logging.getLogger(self.__class__.__name__)

    @Override
    def get_game_config(self,
                        game_id: str) -> Optional[GameNotificationConfig]:
        saved = self._redis.connection.get(f"gameconfig_{game_id}")
        if saved:
            try:
                return self._object_mapper.deserialize(str(saved),
                                                       GameNotificationConfig)
            except Exception as e:
                self._logger.warning(
                    f"Error while deserializing game config for {game_id} {saved}. Reverting to default. {e}"
                )
        return create_default_game_config()

    @Override
    def get_game_id_by_channel_id(self, channel_id: str) -> Optional[str]:
        saved = self._redis.connection.get(f"channel_{channel_id}")
        if saved:
            return str(saved)
        return None

    @Override
    def save_game_config(self, game_id: str, config: GameNotificationConfig):
        self._redis.connection.set(f"gameconfig_{game_id}",
                                   self._object_mapper.serialize(config))
        self._redis.connection.set(f"channel_{config.channel_id}", game_id)
