from abc import ABC, abstractmethod


class MQHelper(ABC):
    @abstractmethod
    def send_event(self, key: str, value: bytes) -> bool:
        pass
