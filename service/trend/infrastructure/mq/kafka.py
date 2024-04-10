import sys
from typing import List

from confluent_kafka import Consumer, KafkaException

from ...domain.gateway import TrendEventConsumer, ConsumeCallback


GROUP_ID = "trend-svr"


class KafkaConsumer(TrendEventConsumer):
    def __init__(self, brokers: List[str], topic: str):
        self.consumer = Consumer(
            {'bootstrap.servers': ','.join(brokers),
             'group.id': GROUP_ID,
             'auto.offset.reset': 'smallest'})
        self.topic = topic
        self.running = False

    def consume_events(self, callback: ConsumeCallback):
        try:
            self.consumer.subscribe([self.topic])
            self.running = True
            while self.running:
                msg = self.consumer.poll(timeout=1.0)  # Poll for messages
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaException._PARTITION_EOF:
                        # End of partition
                        sys.stderr.write('%% {} [{}] reached end at offset {} - {}\n'.format(
                            msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    # Process message
                    callback(msg.key(), msg.value())
        finally:
            self.consumer.close()

    def stop(self):
        self.running = False
