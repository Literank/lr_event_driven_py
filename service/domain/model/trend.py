from datetime import datetime
from dataclasses import dataclass
from typing import List

from .book import Book


@dataclass
class Trend:
    query: str
    books: List[Book]
