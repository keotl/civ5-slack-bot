import logging

from civbot.app.config.config import Config
from civbot.app.service.command_dispatcher import (CommandDispatcher,
                                                   CommandResponse)
from jivago.inject.annotation import Singleton
from jivago.lang.annotations import Inject
from jivago.wsgi.annotations import Resource
from jivago.wsgi.methods import POST
from jivago.wsgi.request.request import Request
from jivago.wsgi.request.response import Response
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey


@Singleton
@Resource("/discord/interaction")
class DiscordInteractionResource(object):

    @Inject
    def __init__(self, config: Config, command_dispatcher: CommandDispatcher):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._public_key = config.discord_public_key
        self._verify_key = VerifyKey(bytes.fromhex(self._public_key or ""))
        self._command_dispatcher = command_dispatcher

    @POST
    def post_interaction(self, req: Request, body: dict):
        signature = req.headers["X-Signature-Ed25519"]
        timestamp = req.headers["X-Signature-Timestamp"]
        body_text = req.body.decode("utf-8")

        try:
            self._verify_key.verify(f'{timestamp}{body_text}'.encode(),
                                    bytes.fromhex(signature))
        except BadSignatureError:
            return Response(401, {}, "")

        if body.get("type") == 1:  # Discord PING
            return {"type": 1}

        if body.get("type") == 2:  # Slash command
            command, params = _parse_discord_slash_command(body)
            response = self._command_dispatcher.dispatch(command, params)
            return _format_discord_response(response)

        self._logger.error(f"Unhandled interaction {body}")


def _parse_discord_slash_command(body: dict):
    command = body.get("data", {}).get("name") or ""
    params = {"channel_id": body.get("channel_id")}
    for option in body.get("data", {}).get("options") or []:
        params[option.get("name") or ""] = option.get("value")
    return command, params


def _format_discord_response(response: CommandResponse):
    if "text" in response:
        return {"type": 4, "data": {"content": response["text"]}}
