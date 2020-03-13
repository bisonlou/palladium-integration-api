import os
import json
import unittest
from flask import Flask
from api.database import create_db, db
from api.models.user import User
from api.controllers.stationery import stationery_module
from api.models.stationery import Stationery

test_app = Flask(__name__)
database_path = os.environ.get("TEST_POSTGRES_DATABASE_URL")
create_db(test_app, database_path)

stationery_module(test_app)


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.client = test_app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_get_stationery_successfuly(self):
        response = self.client.get("/stationery")
        data = response.get_json()

        self.assertTrue(data["success"])
        self.assertEqual(len(data["data"]), 0)

    def test_get_specific_stationery_order_non_existent(self):
        response = self.client.get("/stationery/1")
        self.assertEqual(response.status_code, 404)

    def test_post_stationery_successfuly(self):
        body = {
            "name": "pen",
            "description": "pen",
        }

        response = self.client.post(
            "/stationery",
            data=json.dumps(body),
            content_type='application/json',
        )
        data = response.get_json()

        self.assertTrue(data["success"])
        self.assertEqual(response.status_code, 200)

    def test_post_stationery_without_description_successfuly(self):
        body = {
            "name": "pencil",
            "description": "",
        }

        response = self.client.post(
            "/stationery",
            data=json.dumps(body),
            content_type='application/json',
        )
        data = response.get_json()

        self.assertTrue(data["success"])
        self.assertEqual(response.status_code, 200)

    def test_post_duplicate_stationsery_unsuccessfuly(self):
        body = {
            "name": "pencil",
            "description": "pencil",
        }

        self.client.post(
            "/stationery",
            data=json.dumps(body),
            content_type='application/json',
        )

        response = self.client.post(
            "/stationery",
            data=json.dumps(body),
            content_type='application/json',
        )

        data = response.get_json()

        self.assertFalse(data["success"])
        self.assertEqual(response.status_code, 400)

    def test_update_stationery_successfuly(self):
        body = {
            "name": "pen",
            "description": "pen",
        }

        update_body = {
            "name": "pencil",
            "description": "pencil",
        }

        self.client.post(
            "/stationery",
            data=json.dumps(body),
            content_type='application/json',
        )

        response = self.client.put(
            "/stationery/1",
            data=json.dumps(update_body),
            content_type="application/json"
            )
        data = response.get_json()

        self.assertTrue(data["success"])
        self.assertEqual(update_body["name"], data["data"]["name"])
        self.assertEqual(update_body["description"], data["data"]["description"])
        self.assertEqual(response.status_code, 200)

    def test_update_stationery_when_item_non_existent(self):
        update_body = {
            "name": "pencil",
            "description": "pencil",
        }

        response = self.client.put(
            "/stationery/1",
            data=json.dumps(update_body),
            content_type="application/json"
            )
        data = response.get_json()

        self.assertEqual(response.status_code, 404)

    def test_delete_stationery_successfuly(self):
        body = {
            "name": "pen",
            "description": "pen",
        }

        self.client.post(
            "/stationery",
            data=json.dumps(body),
            content_type='application/json',
        )

        response = self.client.delete("/stationery/1")
        data = response.get_json()

        self.assertTrue(data["success"])
        self.assertEqual(response.status_code, 200)

    def test_delete_non_existent_stationery(self):
        response = self.client.delete("/stationery/1")
        self.assertEqual(response.status_code, 404)
