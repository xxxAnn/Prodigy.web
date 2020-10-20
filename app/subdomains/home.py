import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ..db import get_db

bp = Blueprint('homepage', __name__, url_prefix='')


@bp.route('/', methods=('GET', 'POST'))
def main():
    if request.method == "POST":
        return redirect(url_for('users.view_user', user_id= request.form['searchcontent']))

    return render_template('home.html')