from datetime import datetime

from jivago.inject.annotation import Component


@Component
class Clock(object):

    def now(self) -> datetime:
        return datetime.now()
