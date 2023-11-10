import os
from functools import lru_cache

import yaml
from aiohttp import web
from pydantic import BaseModel

CONFIG_PATH = "SERVICE_CONFIG_PATH"
CONFIG_FILE_NAME = "config.yaml"


class Settings(BaseModel):
    database_url: str
    database_echo: bool


@lru_cache
def _read_settings() -> Settings:
    path_to_yaml = os.getenv(CONFIG_PATH, CONFIG_FILE_NAME)

    with open(path_to_yaml, "r") as f:
        data = yaml.safe_load(f)

    return Settings(**data)


def setup_config(app: web.Application) -> None:
    app["config"] = _read_settings()


def get_settings() -> Settings:
    return _read_settings()
