from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import POST

from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel


@Resource("/civ")
class CivHookResource(object):

    @POST
    def state_endpoint(self, body: CivHookStateModel):
        print(body)
        return "OK"
