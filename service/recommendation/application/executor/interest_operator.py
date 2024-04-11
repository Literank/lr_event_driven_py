from typing import List

from ....domain.model import Interest
from ...domain.gateway import InterestManager


class InterestOperator():

    def __init__(self, interest_manager: InterestManager):
        self.interest_manager = interest_manager

    def interests_for_user(self, user_id: str) -> List[Interest]:
        return self.interest_manager.list_interests(user_id)
