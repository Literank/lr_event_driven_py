import json
from typing import Dict, List

from ....domain.model import Interest
from ...domain.gateway import InterestManager
from ....domain.gateway import TrendEventConsumer


class InterestConsumer():

    def __init__(self, interest_manager: InterestManager, event_consumer: TrendEventConsumer):
        self.interest_manager = interest_manager
        self.event_consumer = event_consumer

    def start(self):
        def process_event(key: bytes, data: bytes):
            parts = key.decode('utf-8').split(':')
            if len(parts) == 1:
                # no user_id, ignore it
                return
            books: List[Dict] = json.loads(data)
            user_id = parts[1]
            for b in books:
                self.interest_manager.increase_interest(Interest(
                    user_id=user_id,
                    title=b['title'],
                    author=b['author'],
                    score=0
                ))
        self.event_consumer.consume_events(process_event)

    def get_event_consumer(self) -> TrendEventConsumer:
        return self.event_consumer
