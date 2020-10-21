import functools
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ..db import get_db

bp = Blueprint('special', __name__, url_prefix='/special')

@bp.route('/search')
def search():
    return redirect(url_for('users.view_user', user_id=request.args.get('q')))

@bp.route('/upload', methods=("POST",))
def upload():
    file = request.files['upfile']
    file.save(os.path.join('app\\uploads', file.filename))
    return redirect(request.referrer)