import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from api.database import create_db
from api.database.finance_services import cursor

load_dotenv()

app = Flask(__name__)
CORS(app)

database_path = os.getenv("POSTGRES_DATABASE_URL")
create_db(app, database_path)

from api.controllers.users import user_module
from api.controllers.errors import errorhandler
from api.controllers.journal import journal_module
from api.controllers.stationery import stationery_module
from api.controllers.stationery_requisition import (
    stationery_requisition_module,
)
from api.controllers.projects import project_module

user_module(app)
errorhandler(app)
journal_module(app)
stationery_module(app)
stationery_requisition_module(app)
project_module(app)
