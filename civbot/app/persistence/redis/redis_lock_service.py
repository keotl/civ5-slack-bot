from civbot.app.persistence.redis.redis_connection import RedisConnection
from civbot.app.service.lock_service import LockService
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject, Override


@Component
class RedisLockService(LockService):

    @Inject
    def __init__(self, redis: RedisConnection):
        self._redis = redis
        self._default_timeout = 5

    @Override
    def game_lock(self, game_id: str):
        return self._redis.connection.lock(f"gamelock_{game_id}",
                                           timeout=self._default_timeout)

    @Override
    def init_lock(self):
        return self._redis.connection.lock(f"initlock",
                                           timeout=self._default_timeout)
