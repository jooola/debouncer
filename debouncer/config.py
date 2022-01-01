from functools import lru_cache
from typing import Dict, Optional

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    port: int = Field(4000, env="PORT")
    store_path: str = Field("debouncer.db", env="STORE_PATH")
    credentials: Optional[Dict[str, str]] = Field(None, env="CREDENTIALS")


@lru_cache()
def get_config():
    return Config()
