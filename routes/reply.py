from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    Request)

from models.message import Messages
from models.user import User
from routes.helper import current_user
from models.topic import Topic
from models.reply import Reply

main = Blueprint('reply', __name__)


def users_from_content(content):
    parts = content.split()
    users = []

    for p in parts:
        if p.startswith('@'):
            username = p[1:]
            u = User.one(username=username)
            print('users_from_content <{}> <{}> <{}>'.format(username, p, parts))
            if u is not None:
                users.append(u)

    return users


def send_mails(sender, receivers, reply_link, reply_content):
    for r in receivers:
        form = dict(
            title=reply_link,
            content=reply_content,
            sender_id=sender.id,
            receiver_id=r.id,
            type='at'
        )
        Messages.new(form)


def send_reply(sender, receiver, reply_link, reply_content):
    form = dict(
        title=reply_link,
        content=reply_content,
        sender_id=sender.id,
        receiver_id=receiver.id,
        type='reply'
    )
    Messages.new(form)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()

    t = Topic.one(id=form['topic_id'])
    user = User.one(id=t.user_id)
    content = form['content']
    users = users_from_content(content)

    send_mails(u, users, form['topic_id'], content)
    send_reply(u, user, form['topic_id'], content)
    form = form.to_dict()
    m = Reply.new(form, user_id=u.id)
    return redirect(url_for('topic.detail', id=m.topic_id))


