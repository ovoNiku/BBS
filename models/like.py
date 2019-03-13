import time

from sqlalchemy import Column, Integer, UnicodeText

from models.base_model import db, SQLMixin
from models.user import User


class Like(SQLMixin, db.Model):
    num = Column(Integer, nullable=False, default=0)
    topic_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    def user(self):
        u = User.one(id=self.user_id)
        return u

    @classmethod
    def new(cls, form, user_id):
        form['user_id'] = user_id
        l = super().new(form)
        return l
