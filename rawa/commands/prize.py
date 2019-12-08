from typing import List, Optional

from rawa.models import db, User, Prize, BoughtPrize


def find_prize(prize_id: int) -> Optional[Prize]:
    return Prize.query.filter_by(id=prize_id).first()


def get_available_prizes(user: User, user_score: int) -> List[Prize]:
    return list(
        Prize.query
        .outerjoin(Prize.bought_prizes)
        .filter(
            BoughtPrize.user != user,
            Prize.score <= user_score,
        )
        .order_by(Prize.score)
    )


def get_bought_prizes(user: User) -> List[Prize]:
    return list(
        Prize.query
        .join(Prize.bought_prizes)
        .filter(BoughtPrize.user == user)
    )


def buy_prize(user: User, prize: Prize) -> BoughtPrize:
    bought_prize = BoughtPrize(user=user, prize=prize)
    db.session.add(bought_prize)
    db.session.commit()
    return bought_prize