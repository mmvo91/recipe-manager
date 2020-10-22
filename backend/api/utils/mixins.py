import sqlalchemy as sql
import sqlalchemy.ext.declarative

from api.utils.db import Base


class Audit(Base):
    __abstract__ = True

    id = sql.Column(sql.Integer, primary_key=True)

    @sql.ext.declarative.declared_attr
    def ModifiedDate(self):
        col = sql.Column(
            sql.DateTime,
            default=sql.sql.func.now(),
            onupdate=sql.sql.func.now(),
            nullable=False,
        )
        col._creation_order = 9990
        return col

    @sql.ext.declarative.declared_attr
    def ModifiedBy(self):
        col = sql.Column(
            sql.String, default="python", onupdate="python", nullable=False
        )
        col._creation_order = 9991

        return col

    @sql.ext.declarative.declared_attr
    def CreatedDate(self):
        col = sql.Column(sql.DateTime, default=sql.sql.func.now(), nullable=False)
        col._creation_order = 9992

        return col

    @sql.ext.declarative.declared_attr
    def CreatedBy(self):
        col = sql.Column(sql.String, default="python", nullable=False)
        col._creation_order = 9993

        return col


class Log(Base):
    __abstract__ = True

    id = sql.Column(sql.Integer, primary_key=True)

    @sql.ext.declarative.declared_attr
    def LogBy(self):
        col = sql.Column(
            sql.String, default="python", onupdate="python", nullable=False
        )
        col._creation_order = 9998

        return col

    @sql.ext.declarative.declared_attr
    def LogDate(self):
        col = sql.Column(
            sql.DateTime,
            default=sql.sql.func.now(),
            onupdate=sql.sql.func.now(),
            nullable=False,
        )
        col._creation_order = 9999

        return col
