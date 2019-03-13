from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
)
import os
import uuid
from models.user import User
from models.topic import Topic
from models.reply import Reply
from routes.helper import login_required, current_user
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
main = Blueprint('user_index', __name__)


@main.route('/<int:id>')
def index(id):
    user = current_user()
    other = User.one(id=id)
    ms = Topic.all(user_id=other.id)
    rs = Reply.all(user_id=other.id)
    topic_set = set()
    for i in rs:
        topic = Topic.one(id=i.topic_id)
        if topic is not None:
            topic_set.add(topic)
    return render_template("user/index.html", user=user, other=other, ms=ms, ts=topic_set, m=None)


@main.route('/edit/<int:id>')
def edit(id):
    u = User.one(id=id)
    return render_template("user/edit.html", user=u)


@main.route('/update', methods=['POST'])
def update():
    form = request.form.to_dict()
    id = int(form['id'])
    u = User.one(id=id)
    u_new = User.update(id, **form)
    if u_new is None:
        return render_template("user/edit.html", user=u, m='f')
    elif u_new == 'already':
        return render_template("user/edit.html", user=u, m='already')
    else:
        return render_template("user/edit.html", user=u_new, m='t')


@main.route('/update/password', methods=['POST'])
def pass_update():
    form = request.form.to_dict()
    id = int(form['id'])
    u = User.one(id=id)
    u_new = User.password_update(id, **form)
    if u_new is None:
        return render_template("user/edit.html", user=u, m='f')
    else:
        return render_template("user/edit.html", user=u_new, m='t')


@main.route('/photo', methods=['post'])
def photo():
    form: FileStorage = request.form.to_dict()
    file = request.files['photo']
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)
    form['img'] = '/' + path

    u = current_user()
    User.img_update(u.id, **form)
    return render_template("user/edit.html", user=u, m='t')

