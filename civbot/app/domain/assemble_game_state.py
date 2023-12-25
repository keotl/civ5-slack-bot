from typing import List, Optional, Tuple

from civbot.app.domain.types import GameState, PlayerState
from civbot.app.resource.civhook.civ_hook_model import (CivHookPlayerModel,
                                                        CivHookStateModel)
from jivago.lang.stream import Stream


def assemble_game_state(payload: CivHookStateModel) -> GameState:
    wars = _assemble_wars(payload.players)
    alliances = _assemble_alliances(payload.players)

    return GameState(
        payload.gameTurn,
        Stream(payload.players).map(lambda p: PlayerState(
            p.id,
            p.nickName,
            p.civilization,
            p.currentEra,
            p.numWonders,
        )).toList(),
        wars,
        alliances,
    )


def _assemble_wars(players: List[CivHookPlayerModel]) -> List[Tuple[int, int]]:
    wars = []
    for player in players:
        for enemy_id in player.enemies:
            enemy = _find_player_by_id(players, int(enemy_id))
            if enemy and int(enemy_id) < player.id:
                wars.append((int(enemy_id), player.id))
    return wars


def _assemble_alliances(
        players: List[CivHookPlayerModel]) -> List[Tuple[int, int]]:
    alliances = []
    for player in players:
        for ally_nickname in player.allies:
            ally = _find_player_by_nickname(players, ally_nickname)
            if ally and ally.id < player.id:
                alliances.append((ally.id, player.id))
    return alliances


def _find_player_by_id(players: List[CivHookPlayerModel],
                       player_id: int) -> Optional[CivHookPlayerModel]:
    for player in players:
        if player.id == player_id:
            return player
    return None


def _find_player_by_nickname(players: List[CivHookPlayerModel],
                             nickname: str) -> Optional[CivHookPlayerModel]:
    for player in players:
        if player.nickName == nickname:
            return player
    return None
