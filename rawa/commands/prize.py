from typing import List

from rawa.models import User, Prize, BoughtPrize


def get_available_prizes(score: int) -> List[Prize]:
    return list(
        Prize.query
        .filter(Prize.score <= score)
        .order_by(Prize.score)
    )


def get_bought_prizes(user: User) -> List[Prize]:
    return list(
        Prize.query
        .join(Prize.bought_prizes)
        .filter(BoughtPrize.user == user)
    )
