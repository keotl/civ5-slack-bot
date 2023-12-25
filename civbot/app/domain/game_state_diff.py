from typing import Iterable, List, Optional, Tuple

from civbot.app.domain.game_events import WarEndedEvent, WarStartedEvent
from civbot.app.domain.selectors import find_player_by_id
from civbot.app.domain.types import GameEvent, GameState
from jivago.lang.stream import Stream


def compute_game_state_diff(old: GameState, new: GameState) -> List[GameEvent]:
    started_wars = _newly_started_wars(old.wars, new.wars)
    ended_wars = _newly_ended_wars(old.wars, new.wars)

    return [
        *Stream(
            started_wars).map(lambda belligerents: _create_war_started_event(
                new, belligerents)).filter(lambda x: x is not None),
        *Stream(ended_wars).map(lambda belligerents: _create_war_ended_event(
            new, belligerents)).filter(lambda x: x is not None)
    ]


def _newly_started_wars(
        old_wars: List[Tuple[int, int]],
        new_wars: List[Tuple[int, int]]) -> Iterable[Tuple[int, int]]:
    for war in new_wars:
        if war in old_wars:
            continue
        yield war


def _newly_ended_wars(
        old_wars: List[Tuple[int, int]],
        new_wars: List[Tuple[int, int]]) -> Iterable[Tuple[int, int]]:
    for war in old_wars:
        if war in new_wars:
            continue
        yield war


def _create_war_started_event(
        game_state: GameState,
        belligerents: Tuple[int, int]) -> Optional[WarStartedEvent]:
    if len(belligerents) != 2:
        return None

    a = find_player_by_id(game_state, belligerents[0])
    b = find_player_by_id(game_state, belligerents[1])

    if a and b:
        return WarStartedEvent([a, b])
    return None


def _create_war_ended_event(
        game_state: GameState,
        belligerents: Tuple[int, int]) -> Optional[WarEndedEvent]:
    if len(belligerents) != 2:
        return None

    a = find_player_by_id(game_state, belligerents[0])
    b = find_player_by_id(game_state, belligerents[1])

    if a and b:
        return WarEndedEvent([a, b])
    return None
