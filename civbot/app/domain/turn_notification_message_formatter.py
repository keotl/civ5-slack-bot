from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel
from jivago.inject.annotation import Component
from jivago.lang.stream import Stream


@Component
class TurnNotificationMessageFormatter(object):

    def format_message(self, state: CivHookStateModel) -> str:
        return f"""Turn: {state.gameTurn}
Remaining players: {', '.join(Stream(state.players).filter(lambda p: p.isHuman and p.isAlive).filter(lambda p: not p.isTurnComplete).map(lambda p: p.nickName))}"""
