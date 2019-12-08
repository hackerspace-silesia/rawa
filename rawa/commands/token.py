from datetime import datetime, date, time
from typing import List
from uuid import uuid4

from PIL.Image import Image
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_H

from rawa.commands.exceptions import CommandError
from rawa.models import db, Station, Token, UsedToken, User


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


def _compute_score_from_token(token: Token) -> int:
    return 100


def use_token(user: User, token_value: str) -> UsedToken:
    token = Token.query.filter_by(value=token_value).first()
    if not token:
        raise CommandError({'token': 'token jest niepoprawny'})

    used_token_before = UsedToken.query.filter_by(user=user, token=token)
    if used_token_before:
        raise CommandError({'token': 'token został już zużyty'})

    used_token = UsedToken(
        user=user,
        token=token,
        score=_compute_score_from_token(token)
    )
    db.session.add(used_token)
    db.session.commit()
    return used_token


def generate_qr_code(token: Token, prefix: str = '') -> Image:
    qrcode = QRCode(error_correction=ERROR_CORRECT_H, border=0)
    qrcode.add_data(prefix + token.value)
    qrcode.make()

    return qrcode.make_image()
