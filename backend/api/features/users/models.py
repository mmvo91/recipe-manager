import sqlalchemy as sql

from api.utils.mixins import Audit


class User(Audit):
    __tablename__ = "users"

    username = sql.Column(sql.String, unique=True)
    email = sql.Column(sql.String)
    password = sql.Column(sql.String)
    active = sql.Column(sql.Boolean, default=False)
    last_login = sql.Column(sql.DateTime)
