from datetime import datetime
from typing import List

from .. import dto
from ...domain.model import Book
from ...domain.gateway import BookManager


class BookOperator():

    def __init__(self, book_manager: BookManager):
        self.book_manager = book_manager

    def create_book(self, b: dto.Book) -> Book:
        book = Book(id=0, created_at=datetime.now(), **b.__dict__)
        id = self.book_manager.create_book(book)
        book.id = id
        return book

    def get_books(self, offset: int, query: str) -> List[Book]:
        return self.book_manager.get_books(offset, query)
