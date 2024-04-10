from typing import List

from ....domain.model import Trend
from ...domain.gateway import TrendManager


class TrendOperator():

    def __init__(self, trend_manager: TrendManager):
        self.trend_manager = trend_manager

    def top_trends(self, page_size: int) -> List[Trend]:
        return self.trend_manager.top_trends(page_size)
