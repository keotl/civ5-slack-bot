from abc import ABC, abstractmethod

from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel


class TurnNotifier(ABC):

    @abstractmethod
    def notify(self, game_id: str, state: CivHookStateModel):
        raise NotImplementedError
