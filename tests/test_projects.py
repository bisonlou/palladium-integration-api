import os
import json
import unittest
from flask import Flask
from api.database import create_db, db
from api.models.user import User
from api.controllers.projects import project_module
from api.models.project import Project


test_app = Flask(__name__)
database_path = os.environ.get("TEST_POSTGRES_DATABASE_URL")
create_db(test_app, database_path)

project_module(test_app)


class ProjectsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = test_app.test_client()
        self.body = {
            "project_name": "census",
            "country": "Uganda",
            "client_name": "GOU",
            "contact_person_name": "Edward",
            "contact_person_title": "CEO",
            "contact_person_tel": "0753668786",
            "start_date": "01-01-2020",
            "end_date": "01-01-2020",
            "contract_value": 100000.00,
            "staff_months": 4.0,
            "consultant_months": 4.0,
            "senior_proffesional": "zachariah","project_description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
            "service_description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
            "remarks": "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
            "associate_consultants": [{
            	"name": "Enoch"
            }]
        }
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_get_projects_successfuly(self):
        response = self.client.get("/projects")
        data = response.get_json()

        self.assertTrue(data["success"])
        self.assertEqual(len(data["data"]), 0)

    def test_get_specified_project_successfuly(self):
        self.client.post(
            "/projects",
            data=json.dumps(self.body),
            content_type='application/json',
        )

        response = self.client.get("/projects/1")
        data = response.get_json()
        
        self.assertTrue(data["success"])

    def test_get_specific_project_non_existent(self):
        response = self.client.get("/projects/1")
        self.assertEqual(response.status_code, 404)

    def test_post_project_successfuly(self):
        response = self.client.post(
            "/projects",
            data=json.dumps(self.body),
            content_type='application/json',
        )
        data = response.get_json()

        self.assertTrue(data["success"])
        self.assertEqual(response.status_code, 200)

    def test_update_project_successfuly(self):
        update_body = {
            "project_name": "census",
            "country": "Uganda",
            "client_name": "GOU",
            "contact_person_name": "Edward",
            "contact_person_title": "CEO",
            "contact_person_tel": "0753668786",
            "start_date": "01-01-2020",
            "end_date": "01-01-2020",
            "contract_value": 100000.00,
            "staff_months": 4.0,
            "consultant_months": 4.0,
            "senior_proffesional": "zachariah","project_description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
            "service_description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
            "associate_consultants": [{
                "name": "Enoch"
            }]
        }

        self.client.post(
            "/projects",
            data=json.dumps(self.body),
            content_type='application/json',
        )

        response = self.client.put(
            "/projects/1",
            data=json.dumps(update_body),
            content_type="application/json"
            )
        data = response.get_json()
        print(data)
        self.assertTrue(data["success"])
        self.assertEqual(update_body["project_name"], data["data"]["project_name"])
        self.assertEqual(update_body["country"], data["data"]["country"])
        self.assertEqual(response.status_code, 200)

    def test_update_project_when_non_existent(self):
        response = self.client.put(
            "/projects/1",
            data=json.dumps(self.body),
            content_type="application/json"
            )

        self.assertEqual(response.status_code, 404)

    def test_delete_project_successfuly(self):
        self.client.post(
            "/projects",
            data=json.dumps(self.body),
            content_type='application/json',
        )

        response = self.client.delete("/projects/1")
        data = response.get_json()

        self.assertTrue(data["success"])
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/projects")
        data = response.get_json()

        self.assertEqual(data["data"], [])

    def test_delete_non_existent_project(self):
        response = self.client.delete("/projects/1")
        self.assertEqual(response.status_code, 404)
