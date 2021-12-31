from functools import lru_cache
from os import PathLike
from typing import List, cast
from uuid import UUID

from sqlitedict import SqliteDict  # type: ignore

from .schema import Endpoint


class Store:
    def __init__(self, path: PathLike):
        self.store = SqliteDict(path, autocommit=True)

    def close(self):
        self.store.close()

    def all(self) -> List[Endpoint]:
        values = cast(List[Endpoint], list(self.store.values()))
        return list(sorted(values, key=lambda x: x.url))

    def save(self, key: UUID, item: Endpoint):
        self.store[str(key)] = item

    def __contains__(self, key: UUID) -> bool:
        return str(key) in self.store

    def get(self, key: UUID) -> Endpoint:
        return cast(Endpoint, self.store[str(key)])

    def delete(self, key: UUID):
        del self.store[str(key)]


@lru_cache()
def get_store(store_path: PathLike):
    return Store(store_path)
