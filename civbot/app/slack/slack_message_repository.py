from typing import Dict

from jivago.inject.annotation import Component, Singleton
from jivago.lang.nullable import Nullable

from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel


@Component
@Singleton
class SlackMessageRepository(object):
    """Keeps a reference to sent Slack notifications."""

    def __init__(self):
        self.content: Dict[str, "SavedMessage"] = {}

    def persist(self, game_id: str, message: "SavedMessage"):
        self.content[game_id] = message

    def find(self, game_id: str) -> Nullable["SavedMessage"]:
        """Returns the message ts."""
        return Nullable(self.content.get(game_id))


class SavedMessage(object):
    def __init__(self, message_ts: str, turn: int, state: CivHookStateModel):
        self.message_ts = message_ts
        self.turn = turn
        self.game_state = state

    def __eq__(self, other):
        return isinstance(other, SavedMessage) and \
               self.message_ts == other.message_ts and \
               self.turn == other.turn
