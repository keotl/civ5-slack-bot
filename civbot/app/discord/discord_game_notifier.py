from civbot.app.discord.discord_client import DiscordClient
from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel
from civbot.app.service.game_config_service import GameConfigService
from civbot.app.service.game_state_notifier import GameStateNotifier
from civbot.app.slack.slack_message_repository import (SavedMessage,
                                                       SlackMessageRepository)
from civbot.app.slack.slack_notification_message_formatter import \
    SlackNotificationMessageFormatter
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject, Override


@Component
class DiscordGameNotifier(GameStateNotifier):

    @Inject
    def __init__(self, discord: DiscordClient,
                 message_formatter: SlackNotificationMessageFormatter,
                 message_repository: SlackMessageRepository,
                 game_config_service: GameConfigService):
        self._discord = discord
        self._formatter = message_formatter
        self._sent_messages_repo = message_repository
        self._game_config_service = game_config_service

    @Override
    def notify(self, game_id: str, state: CivHookStateModel):
        config = self._game_config_service.get_game_config(game_id)
        if config is None or config.notifier != "discord":
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
