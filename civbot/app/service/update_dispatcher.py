from civbot.app.domain.assemble_game_state import assemble_game_state
from civbot.app.domain.game_state_diff import compute_game_state_diff
from civbot.app.domain.game_state_repository import GameStateRepository
from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel
from civbot.app.service.game_event_notifier import GameEventNotifier
from civbot.app.service.lock_service import LockService
from civbot.app.service.turn_notifier import TurnNotifier
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject


@Component
class UpdateDispatcher(object):

    @Inject
    def __init__(self, game_state_repository: GameStateRepository,
                 turn_notifier: TurnNotifier, lock_service: LockService,
                 game_event_notifier: GameEventNotifier):
        self._game_state_repository = game_state_repository
        self._turn_notifier = turn_notifier
        self._lock_service = lock_service
        self._game_event_notifier = game_event_notifier

    def update(self, game_id: str, state: CivHookStateModel):
        self._turn_notifier.notify(game_id, state)
        events = []

        with self._lock_service.game_lock(game_id):
            last_state = self._game_state_repository.get_last_known_game_state(
                game_id)

            if last_state:
                events = compute_game_state_diff(last_state,
                                                 assemble_game_state(state))

            self._game_state_repository.set_last_known_game_state(
                game_id, assemble_game_state(state))

        if events:
            self._game_event_notifier.notify(game_id, events)
