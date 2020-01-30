from flask import Flask
from api.database import cursor
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

import api.controllers.journal
