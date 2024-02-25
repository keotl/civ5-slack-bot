from typing import List

from civbot.app.resource.civhook.civ_hook_model import (CivHookPlayerModel,
                                                        CivHookStateModel)
from jivago.inject.annotation import Component
from jivago.lang.stream import Stream


@Component
class TurnNotificationMessageFormatter(object):

    def format_message(self, state: CivHookStateModel) -> str:
        standby_players = _standby_players(state)
        active_players = _active_players(state)
        return "\n".join([
            f"Turn: {state.gameTurn}",
            f"Remaining players: {', '.join(active_players)}",
            f"Standby: {', '.join(standby_players)}" if standby_players else ""
        ]).strip("\n ")


def _standby_players(state: CivHookStateModel) -> List[str]:
    return _human_players(state).filter(lambda p: not p.isTurnActive).map(
        _nick_name).toList()


def _active_players(state: CivHookStateModel) -> List[str]:
    return _human_players(state).filter(lambda p: p.isTurnActive).map(
        _nick_name).toList()


def _human_players(state: CivHookStateModel) -> Stream[CivHookPlayerModel]:
    return Stream(
        state.players).filter(lambda p: p.isHuman and p.isAlive).filter(
            lambda p: not p.isTurnComplete)


def _nick_name(player: CivHookPlayerModel) -> str:
    return player.nickName
