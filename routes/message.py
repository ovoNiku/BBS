from flask_mail import Message, Mail
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *
from routes.helper import current_user, login_required
from models.message import Messages
from models.reply import Reply
from models.topic import Topic
from config import admin_mail

main = Blueprint('message', __name__)
mail = Mail()


@main.route("/add", methods=["POST"])
@login_required
def add():
    form = request.form.to_dict()
    form['receiver_id'] = int(form['receiver_id'])
    u = current_user()
    form['sender_id'] = u.id

    # 发邮件
    # r = User.one(id=form['receiver_id'])
    # m = Message(
    #     subject=form['title'],
    #     body=form['content'],
    #     sender=admin_mail,
    #     recipients=[r.email]
    # )
    # mail.send(m)

    m = Messages.new(form)
    return redirect(url_for('.index'))


@main.route('/')
@login_required
def index():
    u = current_user()
    message = Messages.all(receiver_id=u.id, type='reply')
    print('message', message)
    t = render_template(
        'message/center.html',
        user=u,
        received=message
    )
    return t


@main.route('/at')
@login_required
def at():
    u = current_user()
    message = Messages.all(receiver_id=u.id, type='at')
    t = render_template(
        'message/at.html',
        user=u,
        received=message
    )
    return t


@main.route('/like')
@login_required
def like():
    u = current_user()
    message = Messages.all(receiver_id=u.id, type='like')
    t = render_template(
        'message/like.html',
        user=u,
        received=message
    )
    return t


# @main.route('/view/<int:id>')
# @login_required
# def view(id):
#     mail = Messages.one(id=id)
#     u = current_user()
    # if u.id == mail.receiver_id or u.id == mail.sender_id:
    # if u.id in [mail.receiver_id, mail.sender_id]:
    #     return render_template('mail/detail.html', mail=mail)
    # else:
    #     return redirect(url_for('.index'))
