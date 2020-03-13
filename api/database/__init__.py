import os
import sys
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import api.models.user
import api.models.stationery
import api.models.project


def create_db(app, database_uri):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    db.create_all()
    migrate = Migrate(app, db)
