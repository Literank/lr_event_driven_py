import logging
import random
import string
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..application.executor import BookOperator
from ..application import WireHelper, dto
from ...domain.model import Book
from ..infrastructure.config.config import RemoteServiceConfig


FIELD_UID = "uid"


def random_string(length):
    random.seed(time.time())  # Using time as seed
    charset = string.ascii_uppercase + "0123456789"
    result = [random.choice(charset) for _ in range(length)]
    return ''.join(result)


class RestHandler:
    def __init__(self, logger: logging.Logger, remote: RemoteServiceConfig, book_operator: BookOperator):
        self._logger = logger
        self.remote = remote
        self.book_operator = book_operator

    def create_book(self, b: dto.Book):
        try:
            return self.book_operator.create_book(b)
        except Exception as e:
            self._logger.error(f"Failed to create: {e}")
            raise HTTPException(status_code=400, detail="Failed to create")

    def get_books(self, offset: int, user_id: str, query: str):
        try:
            books = self.book_operator.get_books(offset, user_id, query)
            return books
        except Exception as e:
            self._logger.error(f"Failed to get books: {e}")
            raise HTTPException(status_code=404, detail="Failed to get books")


def make_router(app: FastAPI, templates_dir: str, remote: RemoteServiceConfig, wire_helper: WireHelper):
    rest_handler = RestHandler(
        logging.getLogger("lr-event"),
        remote,
        BookOperator(wire_helper.book_manager(),
                     wire_helper.message_queue_helper())
    )

    templates = Jinja2Templates(directory=templates_dir)

    @app.get("/", response_class=HTMLResponse)
    async def index_page(request: Request, q: str = ""):
        user_id = request.cookies.get(FIELD_UID)
        if not user_id:
            user_id = random_string(5)
        books = rest_handler.book_operator.get_books(0, user_id, q)
        try:
            trends = rest_handler.book_operator.get_trends(
                rest_handler.remote.trend_url)
        except Exception as e:
            rest_handler._logger.warn(f"Failed to get trends: {e}")
            trends = []
        try:
            interests = rest_handler.book_operator.get_interests(
                rest_handler.remote.rec_url + user_id)
        except Exception as e:
            rest_handler._logger.warn(f"Failed to get interests: {e}")
            interests = []
        resp = templates.TemplateResponse(
            name="index.html", context={
                "request": request,
                "title": "LiteRank Book Store",
                "books": books,
                "trends": trends,
                "recommendations": interests,
                "q": q,
            }
        )
        resp.set_cookie(FIELD_UID, user_id, 3600*24*30)
        return resp

    @app.post("/api/books", response_model=Book)
    async def create_book(b: dto.Book):
        return rest_handler.create_book(b)

    @app.get("/api/books")
    async def get_books(o: int = 0, q: str = ""):
        return rest_handler.get_books(o, "", q)
