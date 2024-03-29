import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import Forbidden

from ..db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

def is_admin():
    if g.user:
        if g.user["AdminLevel"] != None:
            if g.user["AdminLevel"] > 5:
                return True
    return False

def process_command(lvl, d, k, c, v):
    if str.lower(c) == "makeadmin":
        if int(lvl)>int(v):
            db = get_db()
            selected_user = db.execute(
            'SELECT * FROM user WHERE id = ?', (k,)).fetchone()
            if selected_user["AdminLevel"]:
                if selected_user["AdminLevel"]>=int(lvl):
                    return "Unauthorized"
            db.execute('UPDATE user SET AdminLevel = {0} WHERE id = {1}'.format(v, k))
            db.commit()
            return None
        else:
            return "Unauthorized"
    return "Could not parse command"

@bp.route('/commands', methods=("GET", "POST"))
def commands():
    if is_admin():
        error = None
        if request.method == "POST":
            try:
                entity = request.form["Entity"]
                action = request.form["Action"]
                domain = entity.split(":")[0]
                key = entity.split(":")[1]
                command = action.split(":")[0]
                value = action.split(":")[1]
            except:
                error="Could not parse command"
            if error==None:
                error = process_command(g.user["AdminLevel"], domain, key, command, value)
        return render_template('admin/commands.html', errormessage=error or "", successmessage="Success" if error==None else "")
    else:
        return "Unauthorized", 403