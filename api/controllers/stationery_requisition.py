from sys import exc_info
from flask import request, abort, jsonify
from api.models.stationery import (
    Stationery,
    StationeryRequisition,
    StationeryRequisitionDetails,
)
from api.auth import requires_auth


def stationery_requisition_module(app):
    @app.route("/stationery_requisitions")
    def get_all_stationery_requisitions():
        stationery = StationeryRequisition.query.all()

        return jsonify(
            {
                "success": True,
                "data": [item.format_long() for item in stationery],
            }
        )

    @app.route("/stationery_requisitions/<int:requisition_id>")
    def get_requisition(requisition_id):
        requisition = StationeryRequisition.query.first_or_404(requisition_id)
        return jsonify({"success": True, "data": requisition.format_long()})

    @app.route("/stationery_requisitions", methods=["POST"])
    @requires_auth()
    def add_requisition(payload):
        requisition_date = request.json.get("requisition_date", None)
        details = request.json.get("details", None)
        user_id = payload["id"]

        requisition = StationeryRequisition(
            user_id=user_id, requisition_date=requisition_date
        )

        for detail in details:
            item_id = detail["item_id"]
            quantity = detail["quantity"]
            purpose = detail["purpose"]

            requisition_details = StationeryRequisitionDetails(
                item_id=item_id, quantity=quantity, purpose=purpose
            )

            requisition.details.append(requisition_details)

        error = False
        try:
            new_requisition = requisition.add()
        except Exception:
            error = True
            print(exc_info())

        if not error:
            return jsonify(
                {"success": True, "data": new_requisition.format_long()}
            )

    @app.route(
        "/stationery_requisitions/<int:requisition_id>", methods=["PUT"]
    )
    @requires_auth()
    def update_requisition(payload, requisition_id):
        user_id = payload["id"]
        requisition_date = request.json.get("requisition_date", None)
        details = request.json.get("details", None)

        requisition = StationeryRequisition.query.get(requisition_id)

        if not requisition:
            abort(404)

        requisition.requisition_date = requisition_date

        for detail in requisition.details:
            detail.delete()

        for detail in details:
            item_id = detail["item_id"]
            quantity = detail["quantity"]

            requisition_details = StationeryRequisitionDetails(
                item_id=item_id, quantity=quantity
            )

            requisition.details.append(requisition_details)

        error = False
        try:
            updated_requisition = requisition.update()

        except Exception:
            error = True
            print(exc_info())

        if not error:
            return jsonify(
                {"success": True, "data": updated_requisition.format_long()}
            )

    @app.route(
        "/stationery_requisitions/<int:requisition_id>", methods=["DELETE"]
    )
    def delete_requisition(requisition_id):
        requisition = StationeryRequisition.query.get(requisition_id)

        if not requisition:
            abort(404)

        error = False
        try:
            requisition.delete()
        except Exception:
            error = True
            print(exc_info())

        if not error:
            return jsonify({"success": True})
