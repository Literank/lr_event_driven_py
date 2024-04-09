from datetime import datetime

from dataclasses import dataclass


@dataclass
class Book:
    id: int
    title: str
    author: str
    published_at: str
    description: str
    created_at: datetime
