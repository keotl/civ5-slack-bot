from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource
from jivago.wsgi.invocation.parameters import PathParam
from jivago.wsgi.methods import POST

from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel
from civbot.app.service.game_state_notifier import GameStateNotifier


@Resource("/civ/{game_id}")
class CivHookResource(object):

    @Inject
    def __init__(self, notifier: GameStateNotifier):
        self.notifier = notifier

    @POST
    def state_endpoint(self, game_id: PathParam[str], body: CivHookStateModel):
        self.notifier.notify(str(game_id), body)
        return "OK"
