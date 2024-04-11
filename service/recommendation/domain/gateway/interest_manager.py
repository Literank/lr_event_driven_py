from abc import ABC, abstractmethod
from typing import List

from ....domain.model import Interest


class InterestManager(ABC):
    @abstractmethod
    def increase_interest(self, i: Interest):
        pass

    @abstractmethod
    def list_interests(self, user_id: str) -> List[Interest]:
        pass
