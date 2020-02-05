import os
import json
import unittest
from flask import Flask
from dotenv import load_dotenv
from api.controllers.users import user_module
from api.database import create_db, db
from api.models.user import User

load_dotenv()

test_app = Flask(__name__)
database_path = os.getenv("TEST_POSTGRES_DATABASE_URL")
create_db(test_app, database_path)

user_module(test_app)


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.client = test_app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_get_users_successfuly(self):
        response = self.client.get("/users")
        data = response.get_json()

        self.assertTrue(data["success"])
        self.assertEqual(len(data["data"]), 0)

    def test_post_user_successfuly(self):
        body = {
            "email": "test@gmail.com",
            "first_name": "test",
            "last_name": "test",
            "middle_name": "",
            "password": "password",
        }

        response = self.client.post(
            "/users",
            data=json.dumps(body),
            content_type='application/json',
        )
        data = response.get_json()

        self.assertTrue(data["success"])
        self.assertEqual(response.status_code, 200)

    def test_login_successfuly(self):
        body = {
            "email": "test@gmail.com",
            "first_name": "test",
            "last_name": "test",
            "middle_name": "",
            "password": "password",
        }

        self.client.post(
            "/users",
            data=json.dumps(body),
            content_type='application/json',
        )

        body = {
            "email": "test@gmail.com",
            "password": "password"
        }
        response = self.client.post(
            "/login",
            data=json.dumps(body),
            content_type='application/json',
        )
        data = response.get_json()

        self.assertTrue(data["success"])
        self.assertEqual(response.status_code, 200)

    def test_unsuccessful_login(self):
        body = {
            "email": "test@gmail.com",
            "password": "password123"
        }

        response = self.client.post(
            "/login",
            data=json.dumps(body),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 401)
