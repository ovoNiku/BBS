from sqlalchemy import Column, String

from models.base_model import SQLMixin, db
import config
import time


class User(SQLMixin, db.Model):
    username = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)
    signature = Column(String(256), nullable=False, default='这个人很懒，什么都没有填')
    img = Column(String(100), nullable=False, default='/images/timg.jpg')

    @classmethod
    def salted_password(cls, password, salt='$!@><?>HUI&DWQa`'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)

        return hash2

    def hashed_password(self, pwd):
        import hashlib
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and len(pwd) > 2 and User.one(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return u
        elif len(name) < 3 or len(pwd) < 3:
            r = 'f'
            return r
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        user = User.one(username=form['username'])
        if user is not None and user.password == User.salted_password(form['password']):
            return user
        else:
            return None

    @classmethod
    def update(cls, _id, **kwargs):
        if len(kwargs['name']) > 2 and User.one(username=kwargs['name']) is None:
            super().update(
                id=_id,
                username=kwargs['name'],
                signature=kwargs['signature'],
                updated_time=int(time.time())
            )
            u = User.one(id=_id)
            return u
        elif User.one(username=kwargs['name']) is not None:
            r = 'already'
            return r
        else:
            return None

    @classmethod
    def img_update(cls, _id, **kwargs):
        super().update(
            id=_id,
            img=kwargs['img'],
            updated_time=int(time.time())
        )

        u = User.one(id=_id)
        return u

    @classmethod
    def password_update(cls, _id, **kwargs):
        user = User.one(id=_id)
        if user.password == User.salted_password(kwargs['old_pass']):
            super().update(
                id=_id,
                password=User.salted_password(kwargs['new_pass']),
            )
            return user
        else:
            return None
