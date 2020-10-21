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
            db.execute('UPDATE user SET AdminLevel = {0} WHERE id = {1}'.format(v, k))
            db.commit()

@bp.route('/commands', methods=("GET", "POST"))
def commands():
    if is_admin():
        if request.method == "POST":
            entity = request.form["Entity"]
            action = request.form["Action"]
            domain = entity.split(":")[0]
            key = entity.split(":")[1]
            command = action.split(":")[0]
            value = action.split(":")[1]
            print(value)
            process_command(g.user["AdminLevel"], domain, key, command, value)
        return render_template('admin/commands.html')
    else:
        return "Unauthorized", 403