from typing import List, TypedDict

from jivago.inject.annotation import Component


class CommandResponse(TypedDict):
    text: str


@Component
class CommandDispatcher(object):

    def dispatch(self, command: str, params: dict) -> CommandResponse:
        if command == "mute":
            return {"text": "Muting notifications"}
        if command == "unmute":
            return {"text": "Unmuting notifications"}

        return {"text": "Unknown command."}
