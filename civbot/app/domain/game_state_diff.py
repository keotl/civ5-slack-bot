from typing import Iterable, List, Optional, Tuple

from civbot.app.domain.game_events import (PlayerAdvancedEraEvent,
                                           PlayerEliminatedEvent,
                                           PlayerVictoriousEvent,
                                           WarEndedEvent, WarStartedEvent)
from civbot.app.domain.selectors import find_player_by_id
from civbot.app.domain.types import GameEvent, GameState


def compute_game_state_diff(old: GameState, new: GameState) -> List[GameEvent]:
    return [
        *_newly_started_wars(old, new),
        *_newly_ended_wars(old, new),
        *_era_changes(old, new),
        *_player_eliminations(old, new),
        *_player_victorious(old, new),
    ]


def _newly_started_wars(old: GameState,
                        new: GameState) -> Iterable[WarStartedEvent]:
    for war in new.wars:
        if war in old.wars:
            continue
        event = _create_war_started_event(new, war)
        if event:
            yield event


def _newly_ended_wars(old: GameState,
                      new: GameState) -> Iterable[WarEndedEvent]:
    for war in old.wars:
        if war in new.wars:
            continue
        event = _create_war_ended_event(new, war)
        if event:
            yield event


def _era_changes(old: GameState,
                 new: GameState) -> Iterable[PlayerAdvancedEraEvent]:
    for player in new.players:
        old_player = find_player_by_id(old, player.id)
        if old_player and player.currentEra > old_player.currentEra:
            yield PlayerAdvancedEraEvent(player)


def _player_eliminations(old: GameState,
                         new: GameState) -> Iterable[PlayerEliminatedEvent]:
    for player in new.players:
        old_player = find_player_by_id(old, player.id)
        if old_player and not player.isAlive and old_player.isAlive:
            yield PlayerEliminatedEvent(player)


def _player_victorious(old: GameState,
                       new: GameState) -> Iterable[PlayerVictoriousEvent]:
    if old.victory.winner == -1 and new.victory.winner != -1:
        winner = find_player_by_id(new, new.victory.winner)
        if winner:
            yield PlayerVictoriousEvent(winner, new.victory.type)


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
