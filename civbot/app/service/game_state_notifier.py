from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel


class GameStateNotifier(object):

    def notify(self, game_id: str, state: CivHookStateModel):
        raise NotImplementedError
