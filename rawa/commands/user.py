from hashlib import sha1
from os import environ
from typing import Optional
from re import compile as re_compile

from rawa.commands.exceptions import CommandError
from rawa.models import db, User

SALT = environ.get('APP_SALT', 'foobar').encode()
re_email = re_compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def hash_password(password: str) -> str:
    return sha1(SALT + password.encode()).hexdigest()


def login(email: str, password: str) -> Optional[User]:
    return (
        User.query
        .filter_by(
            email=email,
            password=hash_password(password),
        )
        .first()
    )


def find_user(user_id: int) -> Optional[User]:
    return User.query.filter_by(id=user_id).first()


def email_is_valid(email: str) -> bool:
    return re_email.match(email) is not None


def email_is_exists(email: str) -> bool:
    return User.query.filter_by(email=email).first() is not None


def _register_validate(email: str, password: str):
    errs = {}
    if not email:
        errs['email'] = 'email nie powinnien być pusty'
    elif not email_is_valid(email):
        errs['email'] = 'email nie jest poprawny'
    elif email_is_exists(email):
        errs['email'] = 'email istnieje w bazie danych'

    if not password:
        errs['password'] = 'hasło nie powinno być puste'

    if errs:
        raise CommandError(errs)


def register(email: str, password: str) -> User:
    _register_validate(email, password)
    user = User(
        email=email,
        password=hash_password(password),
    )
    db.session.add(user)
    db.session.commit()
    return user
