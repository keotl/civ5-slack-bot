from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource, Path
from jivago.wsgi.invocation.parameters import PathParam
from jivago.wsgi.methods import POST

from civbot.app.slack.slack_message_refresher import SlackMessageRefresher


@Resource("slack")
class SlackCommandResource(object):

    @Inject
    def __init__(self, slack_message_refresher: SlackMessageRefresher):
        self.slack_message_refresher = slack_message_refresher

    @POST
    @Path("/{game_id}")
    def refresh_message(self, game_id: PathParam[str]):
        self.slack_message_refresher.refresh_message(game_id)
        return "OK"
