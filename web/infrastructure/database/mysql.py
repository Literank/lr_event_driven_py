import mysql.connector

from ...domain.gateway import BookManager
from ...domain.model import Book
from ..config import DBConfig


class MySQLPersistence(BookManager):
    def __init__(self, c: DBConfig):
        self.conn = mysql.connector.connect(
            host=c.host,
            port=c.port,
            user=c.user,
            password=c.password,
            database=c.database,
            autocommit=True
        )
        self.cursor = self.conn.cursor(dictionary=True)
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            published_at DATE NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')

    def create_book(self, b: Book) -> int:
        self.cursor.execute('''
            INSERT INTO books (title, author, published_at, description) VALUES (%s, %s, %s, %s)
        ''', (b.title, b.author, b.published_at, b.description))
        return self.cursor.lastrowid or 0
