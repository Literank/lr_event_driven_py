from dataclasses import dataclass


@dataclass
class Book:
    title: str
    author: str
    published_at: str
    description: str
