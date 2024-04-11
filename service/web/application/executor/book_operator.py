from dataclasses import asdict
from datetime import datetime
import json
from typing import Dict, List
import urllib.request


from .. import dto
from ....domain.model import Book, Trend, Interest
from ...domain.gateway import BookManager
from ...infrastructure.mq import MQHelper


class BookOperator():

    def __init__(self, book_manager: BookManager, mq_helper: MQHelper):
        self.book_manager = book_manager
        self.mq_helper = mq_helper

    def create_book(self, b: dto.Book) -> Book:
        book = Book(id=0, created_at=datetime.now(), **b.__dict__)
        id = self.book_manager.create_book(book)
        book.id = id
        return book

    def get_books(self, offset: int, user_id: str, query: str) -> List[Book]:
        books = self.book_manager.get_books(offset, query)
        # Send a user's search query and its results
        if query:
            k = query + ':' + user_id
            json_data = json.dumps([_convert(b)
                                   for b in books]).encode('utf-8')
            self.mq_helper.send_event(k, json_data)
        return books

    def get_trends(self, trend_url: str) -> List[Trend]:
        with urllib.request.urlopen(trend_url) as response:
            data = response.read()
            return json.loads(data.decode('utf-8'))

    def get_interests(self, interests_url: str) -> List[Interest]:
        with urllib.request.urlopen(interests_url) as response:
            return json.loads(response.read().decode('utf-8'))


def _convert(b: Book) -> Dict:
    d = asdict(b)
    d['created_at'] = d['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    return d
