from abc import ABC, abstractmethod

from ..model import Book


class BookManager(ABC):
    @abstractmethod
    def create_book(self, b: Book) -> int:
        pass
