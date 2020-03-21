from jivago.inject.annotation import Component, Singleton


@Component
@Singleton
class SlackMessageRepository(object):
    """Keeps a reference to sent Slack notifications."""

    def persist(self, message):
        pass

    def find(self, game_id: str, turn: int):
        pass
