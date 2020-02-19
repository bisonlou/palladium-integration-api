import os
import json
import unittest
from flask import Flask
from dotenv import load_dotenv
from api.models.user import User
from api.database import create_db, db
from api.models.stationery import Stationery
from api.controllers.stationery import stationery_module
from api.controllers.stationery_requisition import stationery_requisition_module

load_dotenv()

test_app = Flask(__name__)
database_path = os.getenv("TEST_POSTGRES_DATABASE_URL")
create_db(test_app, database_path)

stationery_module(test_app)
stationery_requisition_module(test_app)


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.client = test_app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_get_stationery_requisitions_successfuly(self):
        response = self.client.get("/stationery_requisitions")
        data = response.get_json()

        self.assertTrue(data["success"])
        self.assertEqual(len(data["data"]), 0)

    def test_get_specificstationery_requisitions_successfuly(self):
        response = self.client.get("/stationery_requisitions/1")
        self.assertEqual(response.status_code, 404)
