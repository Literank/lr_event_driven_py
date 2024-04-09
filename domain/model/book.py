from dataclasses import dataclass
from datetime import datetime


@dataclass
class Book:
    id: int
    title: str
    author: str
    published_at: str
    description: str
    created_at: datetime
