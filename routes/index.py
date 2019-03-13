from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
    abort)
from flask.json import jsonify
from models.user import User
from routes.helper import current_user

main = Blueprint('index', __name__)


@main.route("/")
def index():
    u = current_user()
    return render_template("login.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    u = User.register(form)
    if u is None:
        return render_template("login.html", user=u, m='register_f')
    elif u == 'f':
        return render_template("login.html", user=u, m='register_a')
    else:
        return render_template("login.html", user=u, m='register_t')


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return render_template("login.html", user=u, m='login_t')
    else:
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/quit')
def quit():
    session.clear()
    return redirect(url_for('.index'))


@main.route('/images/<filename>')
def image(filename):
    return send_from_directory('images', filename)
