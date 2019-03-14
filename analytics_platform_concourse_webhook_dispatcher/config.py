from sanic_envconfig import EnvConfig


class Config(EnvConfig):
    DEBUG: bool = False
    PORT: int = 8000
    SECRET: str = ""
    CONCOURSE_BASE_URL: str = ""
    CONCOURSE_BASE_URL_DEV: str = ""
    CONCOURSE_TEAM: str = "main"
    CONCOURSE_DEFAULT_RESOURCE: str = "release"
    CONCOURSE_MAIN_USERNAME: str = ""
    CONCOURSE_MAIN_PASSWORD: str = ""
    DEFAULT_EVENT: str = "release"
    FLY_BIN: str = '/home/app/bin/fly'
