from abc import ABC, abstractmethod
from typing import Callable


ConsumeCallback = Callable[[bytes, bytes], None]


class TrendEventConsumer(ABC):
    @abstractmethod
    def consume_events(self, callback: ConsumeCallback):
        pass

    @abstractmethod
    def stop(self):
        pass
