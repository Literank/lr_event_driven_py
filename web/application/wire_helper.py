from ..domain.gateway import BookManager
from ..infrastructure.config import Config
from ..infrastructure.database import MySQLPersistence


class WireHelper:
    def __init__(self, sqlPersistence: MySQLPersistence):
        self.sqlPersistence = sqlPersistence

    @classmethod
    def new(cls, c: Config):
        db = MySQLPersistence(c.db)
        return cls(db)

    def book_manager(self) -> BookManager:
        return self.sqlPersistence
