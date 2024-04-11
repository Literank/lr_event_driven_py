from typing import List

from pymongo import MongoClient, DESCENDING

from ...domain.gateway import InterestManager
from ....domain.model import Interest

COLL_REVIEW = "interests"


class MongoPersistence(InterestManager):
    def __init__(self, uri: str, db_name: str, page_size: int):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.coll = self.db[COLL_REVIEW]
        self.page_size = page_size

    def increase_interest(self, i: Interest):
        filter_query = {
            "user_id": i.user_id,
            "title": i.title,
            "author": i.author,
        }
        update_query = {
            "$inc": {"score": 1}
        }
        self.coll.update_one(filter_query, update_query, upsert=True)

    def list_interests(self, user_id: str) -> List[Interest]:
        filter_query = {"user_id": user_id}
        # Exclude the _id field from the result
        projection = {"_id": 0}
        cursor = self.coll.find(filter_query, projection).sort(
            "score", DESCENDING).limit(self.page_size)
        return list(cursor)
