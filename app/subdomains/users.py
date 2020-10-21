import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ..db import get_db

bp = Blueprint('users', __name__, url_prefix='/users')

def to_admin_level(k):
    if k == 0:
        return "User"
    if 0<k<6:
        return "Moderator"
    elif 5<k<10:
        return "Administrator"
    elif k==10:
        return "Manager"

@bp.route('/<user_id>')
def view_user(user_id):
    error = None
    
    if user_id == "me":
        if g.user:
            user_id = g.user["id"]

    selected_user = get_db().execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

    print(selected_user["AdminLevel"])


    if not selected_user:
        error = "User doesn't exist"
    
    if not error:
        hasadmin = "User" if selected_user["AdminLevel"] == None else to_admin_level(selected_user["AdminLevel"])
        return render_template('user.html', username=selected_user["username"], hasadmin=hasadmin)

    return error