from functools import lru_cache

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    port: int = Field(4000, env="PORT")
    store_path: str = Field("debouncer.db", env="STORE_PATH")


@lru_cache()
def get_config():
    return Config()
