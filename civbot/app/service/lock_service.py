import threading
from typing import Dict

from jivago.inject.annotation import Component, Singleton


@Component
@Singleton
class LockService(object):

    def __init__(self):
        self._lock = threading.Lock()
        self._game_locks: Dict[str, threading.Lock] = {}

    def game_lock(self, game_id: str) -> threading.Lock:
        res = None
        with self._lock:
            if game_id not in self._game_locks:
                self._game_locks[game_id] = threading.Lock()
            res = self._game_locks[game_id]
        return res
