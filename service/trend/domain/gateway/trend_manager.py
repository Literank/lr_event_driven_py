from abc import ABC, abstractmethod
from typing import List

from ....domain.model import Trend


class TrendManager(ABC):
    @abstractmethod
    def create_trend(self, t: Trend) -> int:
        pass

    @abstractmethod
    def top_trends(self, offset: int) -> List[Trend]:
        pass
