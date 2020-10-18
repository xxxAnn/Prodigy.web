import os

from flask import Flask

from .db import init_app, get_db
from .subdomains.auth import bp as auth_bp
from .subdomains.users import bp as users_bp

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'prodigy.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    init_app(app)

    return app