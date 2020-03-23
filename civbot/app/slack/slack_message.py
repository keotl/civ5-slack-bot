class SlackMessage(object):

    def __init__(self, text: str, ts: str = None):
        self.text = text
        self.ts = ts

    def __eq__(self, o):
        return isinstance(o, SlackMessage) and \
            self.text == o.text and \
            self.ts == o.ts
