import threading
from abc import ABC, abstractmethod
from typing import Dict

from jivago.lang.annotations import Override


class LockService(ABC):

    @abstractmethod
    def game_lock(self, game_id: str) -> threading.Lock:
        raise NotImplementedError


class InMemoryLockService(object):

    def __init__(self):
        self._lock = threading.Lock()
        self._game_locks: Dict[str, threading.Lock] = {}

    @Override
    def game_lock(self, game_id: str) -> threading.Lock:
        res = None
        with self._lock:
            if game_id not in self._game_locks:
                self._game_locks[game_id] = threading.Lock()
            res = self._game_locks[game_id]
        return res
