from datetime import datetime, date, time
from typing import List
from uuid import uuid4

from rawa.models import db, Station, Token


def _generate_token(station: Station, timestamp: datetime) -> Token:
    token = Token(
        station=station,
        timestamp=timestamp,
        value=uuid4().hex,
    )
    db.session.add(token)
    return token


def generate_tokens_for_one_day(station: Station, day: date) -> List[Token]:
    hours = range(24)
    tokens = [
        _generate_token(
            station=station,
            timestamp=datetime.combine(day, time(hour))
        )
        for hour in hours
    ]
    db.session.commit()
    return tokens

