import functools
import os
import glob

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_file
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

@bp.route('/<user_id>', methods=("GET",))
def view_user(user_id):

    error = None
    
    if user_id == "me":
        if g.user:
            user_id = g.user["id"]
    
    selected_user = get_db().execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

    if not selected_user:
        error = "User doesn't exist"
    
    isautheduser = None

    if g.user:
        if str(g.user["id"]) == str(user_id):
            isautheduser = True

    if not error:
        hasadmin = "User" if selected_user["AdminLevel"] == None else to_admin_level(selected_user["AdminLevel"])
        return render_template('user.html', username=selected_user["username"], hasadmin=hasadmin, isautheduser=isautheduser, pfp=False, userid=selected_user["id"])

    return error

@bp.route('/<user_id>/pfp', methods=("GET",))
def view_pfp(user_id):

    username = get_db().execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()["username"]

    ddir = os.path.join("app\\uploads", username)

    if os.path.exists(ddir):
        print('ayo')
        if txt := glob.glob(os.path.join(ddir, "Current.*")):
            extension = txt[0].split(".")[1]
            return send_file(os.path.join("uploads", username, "Current."+extension))
    return send_file("static\\images\\defaultprofile.png")
    