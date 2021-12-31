from pathlib import Path

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    port: int = Field(4000, env="PORT")
    store_path: Path = Field("./funnel.db", env="STORE_PATH")


config = Config()
