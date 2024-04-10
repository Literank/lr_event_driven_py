from ..domain.gateway import TrendManager
from ..infrastructure.config import Config
from ..infrastructure.cache import RedisCache


class WireHelper:
    def __init__(self, kvStore: RedisCache):
        self.kvStore = kvStore

    @classmethod
    def new(cls, c: Config):
        kv = RedisCache(c.cache.host, c.cache.port,
                        c.cache.password, c.cache.db)
        return cls(kv)

    def trend_manager(self) -> TrendManager:
        return self.kvStore
