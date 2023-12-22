from typing import Literal, Optional

from jivago.config.properties.application_properties import \
    ApplicationProperties
from jivago.config.properties.system_environment_properties import \
    SystemEnvironmentProperties
from jivago.inject.annotation import Component, Singleton
from jivago.lang.annotations import Inject


@Component
@Singleton
class Config(object):
    notifier: Literal["none", "slack", "discord"]
    discord_token: Optional[str]

    @Inject
    def __init__(self, application: ApplicationProperties,
                 env: SystemEnvironmentProperties):
        self.notifier = env.get("NOTIFIER") or application.get(
            "notifier") or "none"
        self.discord_token = env.get("DISCORD_TOKEN") or application.get(
            "discord_token")
