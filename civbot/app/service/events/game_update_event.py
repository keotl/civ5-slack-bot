from civbot.app.resource.civhook.civ_hook_model import CivHookStateModel


class GameUpdateEvent(object):

    def __init__(self, game_id: str, state: CivHookStateModel):
        self.game_id = game_id
        self.state = state

    def __eq__(self, o):
        return isinstance(o, GameUpdateEvent) and \
            o.game_id == self.game_id and \
            o.state == self.state
