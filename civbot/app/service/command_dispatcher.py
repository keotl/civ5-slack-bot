import logging
from datetime import datetime
from typing import TypedDict

from civbot.app.service.game_config_service import GameConfigService
from civbot.app.util.clock import Clock
from civbot.app.util.parse_duration import parse_duration
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject


class CommandResponse(TypedDict):
    text: str


@Component
class CommandDispatcher(object):

    @Inject
    def __init__(self, game_config_service: GameConfigService, clock: Clock):
        self._game_config_service = game_config_service
        self._clock = clock
        self._logger = logging.getLogger(self.__class__.__name__)

    def dispatch(self, command: str, params: dict) -> CommandResponse:
        if command == "mute":
            game_id = self._game_config_service.get_game_id_by_channel_id(
                params.get("channel_id", "")) or ""
            game = self._game_config_service.get_game_config(game_id)

            if not game:
                return {"text": "Game not found for channel."}

            timeout = parse_duration(params.get("duration"), self._clock.now())

            if params.get("type", "all") in ("all", "turn"):
                game.turn_notifications_muted_until = timeout
            if params.get("type", "all") in ("all", "game"):
                game.game_notifications_muted_until = timeout

            self._game_config_service.save_game_config(game_id, game)

            self._logger.info(
                f"Muted notifications for game {game_id} until {timeout}.")
            return {"text": "Muting notifications"}

        elif command == "unmute":
            game_id = self._game_config_service.get_game_id_by_channel_id(
                params.get("channel_id", "")) or ""
            game = self._game_config_service.get_game_config(game_id)

            if not game:
                return {"text": "Game not found for channel."}

            if params.get("type", "all") in ("all", "turn"):
                game.turn_notifications_muted_until = datetime.min
            if params.get("type", "all") in ("all", "game"):
                game.game_notifications_muted_until = datetime.min

            self._game_config_service.save_game_config(game_id, game)

            self._logger.info(f"Unmuted notifications for game {game_id}.")
            return {"text": "Unmuting notifications"}

        return {"text": "Unknown command."}
