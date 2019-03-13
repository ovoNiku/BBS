import time

from sqlalchemy import Unicode, Column

from models.base_model import db, SQLMixin


class Board(SQLMixin, db.Model):
    title = Column(Unicode(50), nullable=False)
