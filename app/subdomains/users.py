import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ..db import get_db

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/<user_id>')
def view_user(user_id):
    error = None
    selected_user = get_db().execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

    if not selected_user:
        error = "User doesn't exist"
    
    if not error:
        return render_template('user.html', username=selected_user["username"])

    return error