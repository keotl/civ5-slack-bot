from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel
from civbot.app.service.update_dispatcher import UpdateDispatcher
from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource
from jivago.wsgi.invocation.parameters import PathParam
from jivago.wsgi.methods import POST


@Resource("/civ/{game_id}")
class CivHookResource(object):

    @Inject
    def __init__(self, dispatcher: UpdateDispatcher):
        self._dispatcher = dispatcher

    @POST
    def state_endpoint(self, game_id: PathParam[str], body: CivHookStateModel):
        self._dispatcher.update(str(game_id), body)
        return "OK"
