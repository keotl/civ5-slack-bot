import logging

from civbot.app.config.config import Config
from civbot.app.discord.discord_client import DiscordClient
from civbot.app.service.lock_service import LockService
from jivago.config.startup_hooks import PostInit
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject, Override
from jivago.lang.runnable import Runnable


@Component
@PostInit
class RegisterDiscordCommands(Runnable):

    @Inject
    def __init__(self, discord: DiscordClient, config: Config,
                 lock_service: LockService):
        self._discord = discord
        self._notifier = config.notifier
        self._logger = logging.getLogger(self.__class__.__name__)
        self._lock_service = lock_service

    @Override
    def run(self):
        if self._notifier != "discord":
            return
        init_lock = self._lock_service.init_lock()
        has_acquired = init_lock.acquire(blocking=False)
        if not has_acquired:
            return
        try:
            self._discord.register_global_slash_command(
                "mute", "Mute notifications for a period of time.", [{
                    "type":
                        3,
                    "name":
                        "type",
                    "description":
                        "Type of notification to mute. Defaults to 'all'.",
                    "required":
                        False,
                    "choices": [{
                        "name": "all",
                        "value": "all"
                    }, {
                        "name": "game",
                        "value": "game"
                    }, {
                        "name": "turn",
                        "value": "turn"
                    }]
                }, {
                    "type":
                        3,
                    "name":
                        "duration",
                    "description":
                        "Specify to automatically re-enable notifications after a period of time. e.g. '6h', '1d', '1w'",
                    "required":
                        False,
                }])
            self._discord.register_global_slash_command(
                "unmute", "Unmute notifications.", [{
                    "type":
                        3,
                    "name":
                        "type",
                    "description":
                        "Type of notification to mute. Defaults to 'all'.",
                    "required":
                        False,
                    "choices": [{
                        "name": "all",
                        "value": "all"
                    }, {
                        "name": "game",
                        "value": "game"
                    }, {
                        "name": "turn",
                        "value": "turn"
                    }]
                }])
            self._discord.register_global_slash_command(
                "connect", "Connect a game to this channel.", [])

            self._logger.info("Registered discord global commands.")
        finally:
            init_lock.release()
