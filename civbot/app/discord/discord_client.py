import requests
from civbot.app.config.config import Config
from civbot.app.discord.types import DiscordMessage
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject


@Component
class DiscordClient(object):

    @Inject
    def __init__(self, config: Config):
        self._token = config.discord_token

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
