from jivago.event.async_event_bus import AsyncEventBus
from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource
from jivago.wsgi.invocation.parameters import PathParam
from jivago.wsgi.methods import POST

from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel
from civbot.app.service.events.game_update_event import GameUpdateEvent


@Resource("/civ/{game_id}")
class CivHookResource(object):

    @Inject
    def __init__(self, event_bus: AsyncEventBus):
        self.event_bus = event_bus

    @POST
    def state_endpoint(self, game_id: PathParam[str], body: CivHookStateModel):
        self.event_bus.emit(GameUpdateEvent(game_id, body))
        return "OK"
