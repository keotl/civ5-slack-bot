from typing import List

from civbot.app.domain.types import GameEvent, NotificationMessage, PlayerState


class WarStartedEvent(GameEvent):

    def __init__(self, belligerents: List[PlayerState]):
        self.belligerents = belligerents

    def notification_message(self) -> NotificationMessage:
        return {
            "text":
                f"War broke out between {self.belligerents[0].civilization} and {self.belligerents[1].civilization}!"
        }


class WarEndedEvent(GameEvent):

    def __init__(self, belligerents: List[PlayerState]):
        self.belligerents = belligerents

    def notification_message(self) -> NotificationMessage:
        return {
            "text":
                f"Peace was restored between {self.belligerents[0].civilization} and {self.belligerents[1].civilization}!"
        }
