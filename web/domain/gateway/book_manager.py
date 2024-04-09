from abc import ABC, abstractmethod
from typing import List

from ..model import Book


class BookManager(ABC):
    @abstractmethod
    def create_book(self, b: Book) -> int:
        pass

    @abstractmethod
    def get_books(self, offset: int, keyword: str) -> List[Book]:
        pass
