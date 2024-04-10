import logging

from fastapi import FastAPI, HTTPException

from ..application.executor import TrendOperator
from ..application.wire_helper import WireHelper


class RestHandler:
    def __init__(self, logger: logging.Logger, trend_operator: TrendOperator):
        self._logger = logger
        self.trend_operator = trend_operator

    def get_trends(self, offset: int):
        try:
            return self.trend_operator.top_trends(offset)
        except Exception as e:
            self._logger.error(f"Failed to get trends: {e}")
            raise HTTPException(status_code=404, detail="Failed to get trends")


def make_router(app: FastAPI, wire_helper: WireHelper):
    rest_handler = RestHandler(
        logging.getLogger("lr-event"),
        TrendOperator(wire_helper.trend_manager())
    )

    @app.get("/trends")
    async def get_trends(o: int = 0):
        return rest_handler.get_trends(o)
