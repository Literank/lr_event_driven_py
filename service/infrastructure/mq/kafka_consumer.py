import sys
import time
from typing import List

from confluent_kafka import Consumer, KafkaException, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic

from ...domain.gateway import TrendEventConsumer, ConsumeCallback


class KafkaConsumer(TrendEventConsumer):
    def __init__(self, brokers: List[str], topic: str, group_id: str):
        self.consumer = Consumer(
            {'bootstrap.servers': ','.join(brokers),
             'group.id': group_id,
             'auto.offset.reset': 'smallest'})
        self.brokers = brokers
        self.topic = topic
        self.running = False

    def _try_to_create_topic(self, brokers: List[str], topic: str):
        admin_client = AdminClient({'bootstrap.servers': ','.join(brokers)})
        topic_metadata = admin_client.list_topics(timeout=10)
        if topic_metadata.topics.get(topic) is None:
            new_topic = NewTopic(topic, 1, 1)
            admin_client.create_topics([new_topic])
            time.sleep(1)  # Hack: wait for it

    def consume_events(self, callback: ConsumeCallback):
        self._try_to_create_topic(self.brokers, self.topic)
        try:
            self.consumer.subscribe([self.topic])
            self.running = True
            while self.running:
                msg = self.consumer.poll(timeout=1.0)  # Poll for messages
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
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
