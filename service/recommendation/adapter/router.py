import logging

from fastapi import FastAPI, HTTPException

from ..application.executor import InterestOperator
from ..application.wire_helper import WireHelper


class RestHandler:
    def __init__(self, logger: logging.Logger, interest_operator: InterestOperator):
        self._logger = logger
        self.interest_operator = interest_operator

    def get_interests(self, user_id: str):
        try:
            return self.interest_operator.interests_for_user(user_id)
        except Exception as e:
            self._logger.error(f"Failed to get interests for {user_id}: {e}")
            raise HTTPException(
                status_code=404, detail=f"Failed to get interests for {user_id}")


def make_router(app: FastAPI, wire_helper: WireHelper):
    rest_handler = RestHandler(
        logging.getLogger("lr-event"),
        InterestOperator(wire_helper.interest_manager())
    )

    @app.get("/recommendations")
    async def get_interests(uid: str = ""):
        return rest_handler.get_interests(uid)
