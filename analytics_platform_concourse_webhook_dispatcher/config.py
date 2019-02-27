from sanic_envconfig import EnvConfig


class Config(EnvConfig):
    DEBUG: bool = False
    PORT: int = 8000
    SECRET: str = ""
    CONCOURSE_BASE_URL: str = ""
    CONCOURSE_TEAM: str = "main"
    CONCOURSE_DEFAULT_RESOURCE: str = "release"
    CONCOURSE_USERNAME: str = ""
    CONCOURSE_PASSWORD: str = ""
    DEFAULT_EVENT: str = "release"
