from abc import ABC, abstractmethod
from typing import Callable, List

from ....domain.model import Trend

ConsumeCallback = Callable[[bytes, bytes], None]


class TrendManager(ABC):
    @abstractmethod
    def create_trend(self, t: Trend) -> int:
        pass

    @abstractmethod
    def top_trends(self, page_size: int) -> List[Trend]:
        pass


class TrendEventConsumer(ABC):
    @abstractmethod
    def consume_events(self, callback: ConsumeCallback):
        pass

    @abstractmethod
    def stop(self):
        pass
