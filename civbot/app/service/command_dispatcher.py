import logging
import uuid
from datetime import datetime
from typing import TypedDict

from civbot.app.config.config import Config
from civbot.app.service.game_config_service import (GameConfigService,
                                                    create_default_game_config)
from civbot.app.util.clock import Clock
from civbot.app.util.parse_duration import parse_duration
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject


class CommandResponse(TypedDict):
    text: str


@Component
class CommandDispatcher(object):

    @Inject
    def __init__(self, game_config_service: GameConfigService, clock: Clock,
                 config: Config):
        self._game_config_service = game_config_service
        self._clock = clock
        self._logger = logging.getLogger(self.__class__.__name__)
        self._config = config

    def dispatch(self, command: str, params: dict) -> CommandResponse:
        if command == "mute":
            game_id = self._game_config_service.get_game_id_by_channel_id(
                params.get("channel_id", "")) or ""
            game = self._game_config_service.get_game_config(game_id)

            if not game:
                return {"text": "Game not found for channel."}

            timeout = parse_duration(params.get("duration"), self._clock.now())
            notification_type = params.get("type", "all")

            if notification_type in ("all", "turn"):
                game.turn_notifications_muted_until = timeout
            if notification_type in ("all", "game"):
                game.game_notifications_muted_until = timeout

            self._game_config_service.save_game_config(game_id, game)

            self._logger.info(
                f"Muted notifications for game {game_id} until {timeout}.")
            return {
                "text":
                    f"Muting {notification_type} notifications until {timeout}."
            }

        elif command == "unmute":
            game_id = self._game_config_service.get_game_id_by_channel_id(
                params.get("channel_id", "")) or ""
            game = self._game_config_service.get_game_config(game_id)

            if not game:
                return {"text": "Game not found for channel."}
            notification_type = params.get("type", "all")
            if notification_type in ("all", "turn"):
                game.turn_notifications_muted_until = datetime.min
            if notification_type in ("all", "game"):
                game.game_notifications_muted_until = datetime.min

            self._game_config_service.save_game_config(game_id, game)

            self._logger.info(f"Unmuted notifications for game {game_id}.")
            return {"text": f"Unmuting {notification_type} notifications."}
        elif command == "connect":
            game_id = self._game_config_service.get_game_id_by_channel_id(
                params["channel_id"])
            created = False
            if not game_id:
                game_id = str(uuid.uuid4())
                created = True

            game_config = create_default_game_config()
            game_config.channel_id = params["channel_id"]
            game_config.notifier = params["notifier_context"]
            self._game_config_service.save_game_config(game_id, game_config)
            self._logger.info(f"Created game {game_id}.")

            if created:
                return {
                    "text":
                        f"A new game has successfully been created. Connect your civ webhook to {self._config.public_url}/civ/{game_id} and start playing!"
                }
            else:
                return {
                    "text":
                        f"Civbot successfully reconfigured. Connect your civ webhook to {self._config.public_url}/civ/{game_id} and start playing!"
                }

        return {"text": "Unknown command."}
