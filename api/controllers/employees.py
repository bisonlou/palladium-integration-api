import os
import sys
from flask import jsonify, abort, request
from api.database.finance_services import get_employees


def employee_module(app):

    @app.route("/employees")
    def get_all_employees():
        error = False

        try:
            data = get_employees()

            employees = []
            for employee in data:
                employees.append({"name": employee[0]})

        except Exception:
            print(sys.exc_info())

        if not error:
            return jsonify(
                {
                    "success": True,
                    "data": employees,
                }
            )
        abort(422)
