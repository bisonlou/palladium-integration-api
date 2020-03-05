from sys import exc_info
from flask import request, abort, jsonify
from api.models.project import (
    Project,
    AssociateConsultant,
)
from api.database import db


def project_module(app):
    @app.route("/projects")
    def get_all_projects():
        projects = Project.query.all()

        return jsonify(
            {"success": True, "data": [project.format_long() for project in projects],}
        )

    @app.route("/projects/<int:project_id>")
    def get_specified_project(project_id):
        project = Project.query.get(project_id)

        if not project:
            abort(404)

        return jsonify({"success": True, "data": project.format_long()})

    @app.route("/projects", methods=["POST"])
    def add_project():
        project_name = request.json.get("project_name", None)
        country = request.json.get("country", None)
        client_name = request.json.get("client_name", None)
        contact_person_name = request.json.get("contact_person_name", None)
        contact_person_title = request.json.get("contact_person_title", None)
        contact_person_tel = request.json.get("contact_person_tel", None)
        start_date = request.json.get("start_date", None)
        end_date = request.json.get("end_date", None)
        contract_value = request.json.get("contract_value", None)
        staff_months = request.json.get("staff_months", None)
        senior_proffesional = request.json.get("senior_proffesional", None)
        project_description = request.json.get("project_description", None)
        service_description = request.json.get("service_description", None)
        associate_consultants = request.json.get("associate_consultants", None)

        project = Project.query.filter(Project.project_name == project_name).all()

        if project:
            return (
                jsonify({"success": False, "description": "project already exists"}),
                400,
            )

        new_project = Project(
            project_name=project_name,
            country=country,
            client_name=client_name,
            contact_person_name=contact_person_name,
            contact_person_title=contact_person_title,
            contact_person_tel=contact_person_tel,
            start_date=start_date,
            end_date=end_date,
            contract_value=contract_value,
            staff_months=staff_months,
            project_description=project_description,
            service_description=service_description,
            senior_proffesional=senior_proffesional,
        )

        for consultant in associate_consultants:
            new_consultant = AssociateConsultant(name=consultant["name"])
            new_project.associate_consultants.append(new_consultant)

        error = False
        try:
            posted_project = new_project.add()
            print(posted_project)
            posted_project.save()
        except Exception:
            error = True
            print(exc_info())

        if not error:
            return jsonify({"success": True, "data": posted_project.format_long()})

        abort(422)

    @app.route("/projects/<int:project_id>", methods=["PUT"])
    def update_project(project_id):
        project_name = request.json.get("project_name", None)
        country = request.json.get("country", None)
        client_name = request.json.get("client_name", None)
        contact_person_name = request.json.get("contact_person_name", None)
        contact_person_title = request.json.get("contact_person_title", None)
        contact_person_tel = request.json.get("contact_person_tel", None)
        start_date = request.json.get("start_date", None)
        end_date = request.json.get("end_date", None)
        contract_value = request.json.get("contract_value", None)
        staff_months = request.json.get("staff_months", None)
        consultant_months = request.json.get("consultant_months", None)
        senior_proffesional = request.json.get("senior_proffesional", None)
        project_description = request.json.get("project_description", None)
        service_description = request.json.get("service_description", None)
        associate_consultants = request.json.get("associate_consultants", None)

        project = Project.query.get(project_id)

        if not project:
            abort(404)

        project.project_name = project_name
        project.country = country
        project.client_name = client_name
        project.contact_person_name = contact_person_name
        project.contact_person_title = contact_person_title
        project.contact_person_tel = contact_person_tel
        project.start_date = start_date
        project.end_date = end_date
        project.contract_value = contract_value
        project.staff_months = staff_months
        project.project_description = project_description
        project.service_description = service_description
        project.senior_proffesional = senior_proffesional

        for consultant in project.associate_consultants:
            consultant.delete()

        for consultant in associate_consultants:
            updated_associate_consultant = AssociateConsultant(name=consultant["name"])

            project.associate_consultants.append(updated_associate_consultant)

        error = False
        try:
            project.save()

        except Exception:
            error = True
            print(exc_info())

        if not error:
            return jsonify({"success": True, "data": project.format_long()})

        abort(422)

    @app.route("/projects/<int:project_id>", methods=["DELETE"])
    def delete_project(project_id):
        project = Project.query.get(project_id)

        if not project:
            abort(404)

        error = False
        try:
            project.delete()
        except Exception:
            error = True
            print(exc_info())

        if not error:
            return jsonify({"success": True})
