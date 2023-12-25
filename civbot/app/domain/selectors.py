from typing import Optional

from civbot.app.domain.types import GameState, PlayerState


def find_player_by_id(state: GameState,
                      player_id: int) -> Optional[PlayerState]:
    for player in state.players:
        if player.id == player_id:
            return player
    return None
