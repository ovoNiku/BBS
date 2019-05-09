from flask import Flask
from flask_admin.contrib.sqla import ModelView
import config
import secret
import time
from models.base_model import db

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.user import main as user_routes
from routes.board import main as board_routes
from routes.message import main as message_routes, mail


def myfirst(list):
    if len(list) == 0:
        return None
    else:
        return list[0]


def formatte_time(time_stamp):
    local_time = time.localtime(int(time_stamp))
    str_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    return str_time


def date_time(str_time):
    str = str_time.split('-', 1)[1].split(' ')[0]
    return str


def safe_str(str):
    str = str.replace('&quot;', '"')
    str = str.replace('&amp;', '&')
    str = str.replace('&lt;', '<')
    str = str.replace('&gt;', '>')
    str = str.replace('&nbsp;', ' ')
    return str


def configured_app():
    app = Flask(__name__)
    app.secret_key = secret.secret_key

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost:3306/bbs?charset=utf8mb4'.format(
        secret.database_password
    )
    db.init_app(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # app.config['MAIL_SERVER'] = 'smtp.exmail.qq.com'
    # app.config['MAIL_PORT'] = 465
    # app.config['MAIL_USE_SSL'] = True
    # app.config['MAIL_USERNAME'] = config.admin_mail
    # app.config['MAIL_PASSWORD'] = secret.mail_password

    # mail.init_app(app)

    register_routes(app)
    app.template_filter()(myfirst)
    app.template_filter()(formatte_time)
    app.template_filter()(date_time)
    app.template_filter()(safe_str)
    return app


def register_routes(app):
    # 注册蓝图
    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(user_routes, url_prefix='/user_index')
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(message_routes, url_prefix='/message')


if __name__ == '__main__':
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=2000,
        threaded=True,
    )
    app.run(**config)
