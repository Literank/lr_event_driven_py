from dataclasses import dataclass


@dataclass
class Interest:
    user_id: str
    title: str
    author: str
    score: float
