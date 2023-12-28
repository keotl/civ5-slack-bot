from civbot.app.discord.discord_client import DiscordClient
from civbot.app.domain.turn_notification_message_formatter import \
    TurnNotificationMessageFormatter
from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel
from civbot.app.service.game_config_service import GameConfigService
from civbot.app.service.turn_notification_message_repository import (
    SavedMessage, TurnNotificationMessageRepository)
from civbot.app.service.turn_notifier import TurnNotifier
from civbot.app.util.clock import Clock
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject, Override


@Component
class DiscordTurnNotifier(TurnNotifier):

    @Inject
    def __init__(self, discord: DiscordClient,
                 message_formatter: TurnNotificationMessageFormatter,
                 message_repository: TurnNotificationMessageRepository,
                 game_config_service: GameConfigService, clock: Clock):
        self._discord = discord
        self._formatter = message_formatter
        self._sent_messages_repo = message_repository
        self._game_config_service = game_config_service
        self._clock = clock

    @Override
    def notify(self, game_id: str, state: CivHookStateModel):
        config = self._game_config_service.get_game_config(game_id)
        if (config is None or config.notifier != "discord"
                or config.turn_notifications_muted_until > self._clock.now()):
            return

        sent = self._sent_messages_repo.find(game_id)

        if sent.isPresent() and sent.get().turn < state.gameTurn:
            self._discord.delete_message(config.channel_id,
                                         sent.get().message_ts)
        elif sent.isPresent() and sent.get().turn == state.gameTurn:
            self._discord.edit_message(config.channel_id,
                                       sent.get().message_ts,
                                       self._formatter.format_message(state))
            return

        message = self._discord.create_message(
            config.channel_id, self._formatter.format_message(state))
        self._sent_messages_repo.persist(
            game_id, SavedMessage(message["id"], state.gameTurn))
