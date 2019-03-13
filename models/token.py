from sqlalchemy import Column, String, Integer

from models.base_model import SQLMixin, db
from models.user import User


class Token(SQLMixin, db.Model):
    token = Column(String(100), nullable=False)
    user_id = Column(Integer, nullable=False)

    @classmethod
    def new(cls, form, user_id):
        form['user_id'] = user_id
        m = super().new(form)
        return m
