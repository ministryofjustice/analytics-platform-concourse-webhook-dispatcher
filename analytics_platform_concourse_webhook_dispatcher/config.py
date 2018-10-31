from pathlib import Path

from sanic_envconfig import EnvConfig


class Config(EnvConfig):
    DEBUG: bool = False
    PORT: int = 8000
    SECRET: str = ""
    CONCOURSE_BASE_URL: str = ""
    CONCOURSE_WEBHOOK_TOKEN: str = ""
    CONCOURSE_TEAM: str = "main"
    CONCOURSE_DEFAULT_RESOURCE: str = "release"
    DEFAULT_EVENT: str = "release"


@Config.parse(Path)
def parse_path(value):
    return Path(value)
