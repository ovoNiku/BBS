import time

from sqlalchemy import Column, Unicode, UnicodeText, Integer, String

from models.base_model import SQLMixin, db
from models.user import User
from models.topic import Topic

class Messages(SQLMixin, db.Model):
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)
    type = Column(String(10), nullable=False)

    def user(self):
        u = User.one(id=self.sender_id)
        return u

    def topic(self):
        t = Topic.one(id=str(self.title))
        return t