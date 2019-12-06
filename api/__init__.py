from flask import Flask
from api.database import cursor

app = Flask(__name__)

import api.controllers.journal
