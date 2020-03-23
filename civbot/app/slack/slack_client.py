import requests
from jivago.config.properties.application_properties import ApplicationProperties
from jivago.inject.annotation import Component
from jivago.lang.annotations import Inject

from civbot.app.slack.slack_message import SlackMessage


@Component
class SlackClient(object):

    @Inject
    def __init__(self, application_properties: ApplicationProperties):
        self.slack_token = application_properties["slack_token"]
        self.slack_channel = application_properties["slack_channel"]

    def post_message_or_update(self, message: SlackMessage) -> SlackMessage:
        if message.ts:
            res = requests.post("https://slack.com/api/chat.update",
                                data={
                                    "token": self.slack_token,
                                    "text": message.text,
                                    "channel": self.slack_channel,
                                    "ts": message.ts
                                })
            return SlackMessage(message.text, res.json()["ts"])
        else:
            requests.post("https://slack.com/api/chat.postMessage",
                          data={
                              "token": self.slack_token,
                              "channel": self.slack_channel,
                              "text": message.text,
                          })
            return message
