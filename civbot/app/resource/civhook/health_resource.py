from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import GET


@Resource("/health")
class HealthResource(object):

    @GET
    def get(self):
        return {"status": "ok"}
