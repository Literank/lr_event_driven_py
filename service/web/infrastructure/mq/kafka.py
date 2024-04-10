from typing import List

from confluent_kafka import Producer

from .helper import MQHelper


class KafkaQueue(MQHelper):
    def __init__(self, brokers: List[str], topic: str):
        self.producer = Producer({'bootstrap.servers': ','.join(brokers)})
        self.topic = topic

    def send_event(self, key: str, value: bytes) -> bool:
        self.producer.produce(self.topic, value, key)
        return True
