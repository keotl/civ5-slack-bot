import logging
from typing import List, NotRequired, TypedDict, Union

import requests
from civbot.app.config.config import Config
from civbot.app.discord.types import DiscordMessage
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject


class DiscordCommandOptionChoice(TypedDict):
    name: str
    value: Union[str, int, float]


class DiscordCommandOptions(TypedDict):
    type: int
    name: str
    description: str
    required: bool
    choices: NotRequired[List[DiscordCommandOptionChoice]]


@Component
class DiscordClient(object):

    @Inject
    def __init__(self, config: Config):
        self._token = config.discord_token
        self._app_id = config.discord_app_id
        self._logger = logging.getLogger(self.__class__.__name__)

    def create_message(self,
                       channel: str,
                       message: str,
                       *,
                       tts: bool = False) -> DiscordMessage:
        res = requests.post(
            f"https://discord.com/api/channels/{channel}/messages",
            headers={
                "Authorization":
                    f"Bot {self._token}",
                "User-Agent":
                    "DiscordBot (https://github.com/keotl/civ5-slack-bot, 0.0.0)",
            },
            json={
                "content": message,
                "tts": tts,
                "embeds": []
            })
        if not res.ok:
            self._logger.error(f"create message: {res.status_code} - {res.text}")
        return res.json()

    def edit_message(self, channel: str, message_id: str,
                     new_content: str) -> DiscordMessage:
        res = requests.patch(
            f"https://discord.com/api/channels/{channel}/messages/{message_id}",
            headers={
                "Authorization":
                    f"Bot {self._token}",
                "User-Agent":
                    "DiscordBot (https://github.com/keotl/civ5-slack-bot, 0.0.0)",
            },
            json={
                "content": new_content,
                "tts": False,
                "embeds": []
            })
        return res.json()

    def delete_message(self, channel: str, message_id):
        requests.delete(
            f"https://discord.com/api/channels/{channel}/messages/{message_id}",
            headers={
                "Authorization":
                    f"Bot {self._token}",
                "User-Agent":
                    "DiscordBot (https://github.com/keotl/civ5-slack-bot, 0.0.0)",
            })

    def register_global_slash_command(self, name: str, description: str,
                                      options: List[DiscordCommandOptions]):
        res = requests.post(
            f"https://discord.com/api/applications/{self._app_id}/commands",
            headers={
                "Authorization":
                    f"Bot {self._token}",
                "User-Agent":
                    "DiscordBot (https://github.com/keotl/civ5-slack-bot, 0.0.0)",
            },
            json={
                "name": name,
                "description": description,
                "type": 1,
                "options": options
            })
        if not res.ok:
            self._logger.warning(f"Register command: {res.status_code} - {res.text}")
