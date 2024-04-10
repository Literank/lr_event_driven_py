import json
from typing import Any, List

import redis

from ...domain.gateway import TrendManager
from ....domain.model import Trend

trends_key = "trends"
query_key_prefix = "q-"


class RedisCache(TrendManager):
    def __init__(self, host: str, port: int, password: str, db: int):
        self.c = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )

    def create_trend(self, t: Trend) -> int:
        member = t.query
        score: Any = self.c.zincrby(trends_key, 1, member)

        k = query_key_prefix + t.query
        results = json.dumps(t.books)
        self.c.set(k, results)
        return score

    def top_trends(self, offset: int) -> List[Trend]:
        top_items: Any = self.c.zrevrange(
            trends_key, 0, offset, withscores=True)
        trends = []
        for item in top_items:
            query = item[0]
            t = Trend(query=query, books=[], created_at=None)
            k = query_key_prefix + query
            value: Any = self.c.get(k)
            if value is not None:
                t.books = json.loads(value)
            trends.append(t)
        return trends
