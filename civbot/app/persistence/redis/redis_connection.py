import logging
from typing import cast

from civbot.app.config.config import Config
from jivago.inject.annotation import Component, Singleton
from jivago.lang.annotations import Inject

import redis


@Component
@Singleton
class RedisConnection(object):
    connection: redis.Redis
    
    @Inject
    def __init__(self, config: Config):
        self._logger = logging.getLogger(self.__class__.__name__)
        if not config.redis_url:
            self._logger.fatal(f"Missing REDIS_URL environment variable.")
            raise Exception(f"Missing REDIS_URL environment variable.")

        self.connection = cast(redis.Redis, redis.from_url(config.redis_url))
        self.connection.ping()
        self._logger.info("Established Redis connection.")
