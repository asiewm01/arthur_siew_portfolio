# flask_app/app/db_app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

from flask_app.settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from flask_app.models import db
from flask_app.app.app import main_bp
from flask_app.app.scratch_app import scratch_bp
from flask_app.app.auth_app import auth_bp


csrf = CSRFProtect()  # ✅ CSRF protection

def create_app():
    app = Flask(
        __name__, 
        static_folder='../static',         # Go up to flask_app/static
        template_folder='templates')

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    # ✅ Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    csrf.init_app(app)

    # ✅ Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(scratch_bp)
    app.register_blueprint(auth_bp)

    return app

app = create_app()
