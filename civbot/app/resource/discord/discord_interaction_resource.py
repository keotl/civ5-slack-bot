import logging

from civbot.app.config.config import Config
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
    def __init__(self, config: Config):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._public_key = config.discord_public_key
        self._verify_key = VerifyKey(bytes.fromhex(self._public_key or ""))

    @POST
    def post_interaction(self, req: Request, body: dict):
        self._logger.info(f"Got interaction {req.headers.content} {body}")

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

        self._logger.error(f"Unhandled interaction {body}")
