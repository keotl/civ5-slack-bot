from typing import List

from jivago.lang.annotations import Override

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


class PlayerAdvancedEraEvent(GameEvent):

    def __init__(self, player: PlayerState):
        self.player = player

    def notification_message(self) -> NotificationMessage:
        return {
            "text":
                f"{self.player.civilization.title()} has entered the {self._era_name()} era!"
        }

    def _era_name(self) -> str:
        return {
            0: "Ancient",
            1: "Classical",
            2: "Medieval",
            3: "Renaissance",
            4: "Industrial",
            5: "Modern",
            6: "Future",
            7: "Postmodern",
        }.get(self.player.currentEra) or "???"

class PlayerEliminatedEvent(GameEvent):
    def __init__(self, player: PlayerState):
        self.player = player

    @Override
    def notification_message(self) -> NotificationMessage:
        return {
            "text": f"{self.player.civilization} has been eliminated!"
        }
