from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import MetaData

db = SQLAlchemy(
    metadata=MetaData(
        naming_convention={
            "ix": 'ix_%(column_0_label)s',
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(column_0_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s"
        }
    )
)


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

class User(Base):
    __abstract__ = False
    email = db.Column(db.String(128), nullable=False, index=True)
    password = db.Column(db.String(128))


class Station(Base):
    __abstract__ = False
    name = db.Column(db.String(128), nullable=False, index=True)
    score = db.Column(db.Integer, nullable=False)


class Token(Base):
    __abstract__ = False
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.String(128))

    station = relationship(Station, backref='tokens')


class UsedToken(Base):
    __abstract__ = False
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token_id = db.Column(db.Integer, db.ForeignKey('token.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    user = relationship(User, backref='used_tokens')
    token = relationship(Token, backref='used_tokens')


class Prize(Base):
    __abstract__ = False
    name = db.Column(db.String(128))
    logo = db.Column(db.String(128))
    description = db.Column(db.String(128))
    score = db.Column(db.Integer)
