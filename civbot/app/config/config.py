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
    discord_app_id: Optional[str]
    discord_token: Optional[str]
    discord_public_key: Optional[str]

    persistence_provider: Literal["none", "redis"]
    redis_url: Optional[str]

    @Inject
    def __init__(self, application: ApplicationProperties,
                 env: SystemEnvironmentProperties):
        self.notifier = env.get("NOTIFIER") or application.get(
            "notifier") or "none"
        self.discord_token = env.get("DISCORD_TOKEN") or application.get(
            "discord_token")
        self.discord_app_id = env.get("DISCORD_APP_ID") or application.get(
            "discord_app_id")
        self.discord_public_key = env.get(
            "DISCORD_PUBLIC_KEY") or application.get("discord_public_key")

        self.persistence_provider = env.get(
            "PERSISTENCE_PROVIDER") or application.get(
                "persistence_provider") or "none"
        self.redis_url = env.get("REDIS_URL") or application.get("redis_url")
