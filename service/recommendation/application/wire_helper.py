from ..domain.gateway import InterestManager
from ...domain.gateway import TrendEventConsumer
from ..infrastructure.config import Config
from ..infrastructure.database import MongoPersistence
from ...infrastructure.mq import KafkaConsumer


class WireHelper:
    def __init__(self, noSQLPersistence: MongoPersistence, consumer: KafkaConsumer):
        self.noSQLPersistence = noSQLPersistence
        self.consumer = consumer

    @classmethod
    def new(cls, c: Config):
        mdb = MongoPersistence(
            c.db.mongo_uri, c.db.mongo_db_name, c.app.page_size)
        consumer = KafkaConsumer(c.mq.brokers, c.mq.topic, c.mq.group_id)
        return cls(mdb, consumer)

    def interest_manager(self) -> InterestManager:
        return self.noSQLPersistence

    def trend_event_consumer(self) -> TrendEventConsumer:
        return self.consumer
