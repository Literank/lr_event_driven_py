from typing import List

from ....domain.model import Trend
from ...domain.gateway import TrendManager


class TrendOperator():

    def __init__(self, trend_manager: TrendManager):
        self.trend_manager = trend_manager

    def create_trend(self, t: Trend) -> int:
        return self.trend_manager.create_trend(t)

    def top_trends(self, offset: int) -> List[Trend]:
        return self.trend_manager.top_trends(offset)
