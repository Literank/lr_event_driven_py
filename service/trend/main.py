from contextlib import asynccontextmanager
import threading

from fastapi import FastAPI

from .adapter.router import make_router
from .application import WireHelper
from .application.consumer import TrendConsumer
from .infrastructure.config import parseConfig

CONFIG_FILENAME = "service/trend/config.yml"

c = parseConfig(CONFIG_FILENAME)
wire_helper = WireHelper.new(c)

# Run the consumer
tc = TrendConsumer(wire_helper.trend_manager(),
                   wire_helper.trend_event_consumer())
event_consumer = tc.get_event_consumer()
consumer_thread = threading.Thread(target=tc.start)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run at startup
    consumer_thread.start()
    yield
    # Run on shutdown
    event_consumer.stop()
    consumer_thread.join()
    print("Event consumer is closed! Bye!")

# Run the FastAPI server
app = FastAPI(lifespan=lifespan)
make_router(app, wire_helper)
