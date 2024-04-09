from typing import Any, List

import mysql.connector

from ...domain.gateway import BookManager
from ...domain.model import Book
from ..config import DBConfig


class MySQLPersistence(BookManager):
    def __init__(self, c: DBConfig, page_size: int):
        self.page_size = page_size
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

    def get_books(self, offset: int, keyword: str) -> List[Book]:
        query = "SELECT * FROM books"
        params: List[Any] = []
        if keyword:
            query += " WHERE title LIKE %s OR author LIKE %s OR description LIKE %s"
            params = [f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"]
        query += " LIMIT %s, %s"
        params.extend([offset, self.page_size])

        self.cursor.execute(query, tuple(params))
        results: List[Any] = self.cursor.fetchall()
        return [Book(**result) for result in results]
