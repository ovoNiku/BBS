from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.board import Board
from routes.helper import current_user

main = Blueprint('board', __name__)


@main.route("/admin")
def index():
    return render_template('board/admin_index.html')


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    current_user()
    Board.new(form)
    return redirect(url_for('topic.index'))

