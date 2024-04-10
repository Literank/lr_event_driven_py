from fastapi import FastAPI

from .adapter.router import make_router
from .application import WireHelper
from .infrastructure.config import parseConfig

CONFIG_FILENAME = "service/trend/config.yml"

c = parseConfig(CONFIG_FILENAME)
wire_helper = WireHelper.new(c)
app = FastAPI()
make_router(app, wire_helper)
