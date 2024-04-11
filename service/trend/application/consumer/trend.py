import json

from ....domain.model import Trend
from ...domain.gateway import TrendManager
from ....domain.gateway import TrendEventConsumer


class TrendConsumer():

    def __init__(self, trend_manager: TrendManager, event_consumer: TrendEventConsumer):
        self.trend_manager = trend_manager
        self.event_consumer = event_consumer

    def start(self):
        def process_event(key: bytes, data: bytes):
            t = Trend(query=key.decode('utf-8'), books=json.loads(data))
            self.trend_manager.create_trend(t)

        self.event_consumer.consume_events(process_event)

    def get_event_consumer(self) -> TrendEventConsumer:
        return self.event_consumer
