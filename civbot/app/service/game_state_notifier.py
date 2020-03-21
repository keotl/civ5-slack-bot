from jivago.event.config.annotations import EventHandler, EventHandlerClass
from jivago.lang.annotations import Inject

from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel
from civbot.app.service.events.game_update_event import GameUpdateEvent


class GameStateNotifier(object):

    def notify(self, game_id: str, state: CivHookStateModel):
        raise NotImplementedError


@EventHandlerClass
class NotificationWorker(object):

    @Inject
    def __init__(self, notifier: GameStateNotifier):
        self.notifier = notifier

    @EventHandler("game_update")
    def handle(self, payload: GameUpdateEvent):
        self.notifier.notify(payload.game_id, payload.state)
