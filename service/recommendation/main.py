import signal

from .application import WireHelper
from .application.consumer import InterestConsumer
from .infrastructure.config import parseConfig

CONFIG_FILENAME = "service/recommendation/config.yml"

c = parseConfig(CONFIG_FILENAME)
wire_helper = WireHelper.new(c)

# Run the consumer
tc = InterestConsumer(wire_helper.interest_manager(),
                      wire_helper.trend_event_consumer())
event_consumer = tc.get_event_consumer()


def sigterm_handler(signal, frame):
    event_consumer.stop()
    print("Consumer stopped. Exiting gracefully...")


signal.signal(signal.SIGTERM, sigterm_handler)
signal.signal(signal.SIGINT, sigterm_handler)

print("Started to consume events...")
tc.start()
