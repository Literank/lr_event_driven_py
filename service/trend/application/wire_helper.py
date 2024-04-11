from ..domain.gateway import TrendManager
from ...domain.gateway import TrendEventConsumer
from ..infrastructure.config import Config
from ..infrastructure.cache import RedisCache
from ...infrastructure.mq import KafkaConsumer


class WireHelper:
    def __init__(self, kvStore: RedisCache, consumer: KafkaConsumer):
        self.kvStore = kvStore
        self.consumer = consumer

    @classmethod
    def new(cls, c: Config):
        kv = RedisCache(c.cache.host, c.cache.port,
                        c.cache.password, c.cache.db)
        consumer = KafkaConsumer(c.mq.brokers, c.mq.topic, c.mq.group_id)
        return cls(kv, consumer)

    def trend_manager(self) -> TrendManager:
        return self.kvStore

    def trend_event_consumer(self) -> TrendEventConsumer:
        return self.consumer
