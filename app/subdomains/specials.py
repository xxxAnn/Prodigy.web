import functools
import os
import glob

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ..db import get_db

bp = Blueprint('special', __name__, url_prefix='/special')

@bp.route('/search')
def search():
    if str(request.args.get('q')).isnumeric():
        return redirect(url_for('users.view_user', user_id=request.args.get('q')))
    else:
        selected_user = get_db().execute(
        'SELECT * FROM user WHERE username = ?', (str(request.args.get('q')),)
        ).fetchone()
        return redirect(url_for('users.view_user', user_id=selected_user["id"]))

@bp.route('/upload', methods=("POST",))
def upload():
    if not g.user:
        return redirect(request.referrer)
    file = request.files['upfile']
    to_create = os.path.join("app\\uploads", g.user["username"])

    if not os.path.exists(to_create):
        os.mkdir(to_create)

    try:
        extension = str(file.filename).split(".")[1]
        if list_dir := glob.glob(os.path.join(to_create, "Current.*")):
            for filepath in list_dir:
                os.remove(filepath)

        file.save(os.path.join(to_create, "Current."+extension))
    finally:
        return redirect(request.referrer)
    