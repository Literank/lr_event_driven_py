from ..domain.gateway import BookManager
from ..infrastructure.config import Config
from ..infrastructure.database import MySQLPersistence
from ..infrastructure.mq import KafkaQueue, MQHelper


class WireHelper:
    def __init__(self, sqlPersistence: MySQLPersistence, mq: KafkaQueue):
        self.sqlPersistence = sqlPersistence
        self.mq = mq

    @classmethod
    def new(cls, c: Config):
        db = MySQLPersistence(c.db, c.app.page_size)
        mq = KafkaQueue(c.mq.brokers, c.mq.topic)
        return cls(db, mq)

    def book_manager(self) -> BookManager:
        return self.sqlPersistence

    def message_queue_helper(self) -> MQHelper:
        return self.mq
