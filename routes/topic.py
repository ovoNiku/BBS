from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.topic import Topic
from models.board import Board
from models.user import User
from routes.helper import current_user, csrf_required, new_csrf_token, login_required
from models.message import Messages
from models.like import Like
import redis

main = Blueprint('topic', __name__)


@main.route("/")
@login_required
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    token = new_csrf_token()
    bs = Board.all()
    u = current_user()
    return render_template("topic/index.html", user=u, ms=ms, bs=bs, bid=board_id, token=token)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    u = current_user()
    l = Like.one(topic_id=m.id, user_id=u.id)
    return render_template("topic/detail.html", topic=m, user=u, l=l)


@main.route('/<int:id>/like')
def detail_like(id):
    m = Topic.get(id)
    u = current_user()
    l = Like.one(topic_id=m.id, user_id=u.id)
    return render_template("topic/like.html", topic=m, user=u, l=l)


@main.route("/delete")
@csrf_required
def delete():
    id = int(request.args.get('id'))
    u = current_user()
    Topic.delete(id)
    return redirect(url_for('.index'))


@main.route("/new")
def new():
    board_id = int(request.args.get('board_id'))
    bs = Board.all()
    user = current_user()
    token = new_csrf_token()
    return render_template("topic/new.html", bs=bs, bid=board_id, user=user, token=token)


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    Topic.new(form, user_id=u.id)
    return redirect(url_for('.index'))


def send_like(sender, receiver, reply_link, reply_content):
    form = dict(
        title=reply_link,
        content=reply_content,
        sender_id=sender.id,
        receiver_id=receiver.id,
        type='like'
    )
    Messages.new(form)


@main.route("/like")
def add_like():
    id = int(request.args.get('id'))
    u = current_user()

    t = Topic.one(id=id)
    user = User.one(id=t.user_id)

    form = {
        'topic_id': t.id,
        'num': 1
    }
    l = Like.one(topic_id=t.id, user_id=u.id)
    if l is None:
        Like.new(form, u.id)
        send_like(u, user, id, '')
    else:
        Like.delete(l.id)
    return redirect(url_for('.detail_like', id=t.id))
