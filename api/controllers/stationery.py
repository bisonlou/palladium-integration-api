from sys import exc_info
from flask import request, abort, jsonify
from api.models.stationery import (
    Stationery,
    StationeryRequisition,
    StationeryRequisitionDetails,
)
from api.database import db


def stationery_module(app):
    @app.route("/stationery")
    def get_all_stationery():
        stationery = Stationery.query.all()

        return jsonify(
            {
                "success": True,
                "data": [item.format_long() for item in stationery],
            }
        )

    @app.route("/stationery/<int:item_id>")
    def get_specified_item(item_id):
        item = Stationery.query.first_or_404(item_id)

        return jsonify({"success": True, "data": item.format_long()})

    @app.route("/stationery", methods=["POST"])
    def add_item():
        name = request.json.get("name", None)
        description = request.json.get("description", None)

        item = Stationery.query.filter(Stationery.name == name).all()

        if item:
            return (
                jsonify(
                    {"success": False, "description": "item already exists"}
                ),
                400,
            )

        item = Stationery(name=name, description=description)

        error = False
        try:
            new_item = item.add()
            db.session.commit()
        except Exception:
            error = True
            print(exc_info())

        if not error:
            return jsonify({"success": True, "data": new_item.format_long()})

    @app.route("/stationery_uploads", methods=["POST"])
    def bulk_item_upload():
        items = request.json.get("items", None)

        stationery = []
        for item in items:
            name = item["name"]
            description = item["description"]

            if not Stationery.query.filter(Stationery.name == name).first():
                stationery.append(
                    Stationery(name=name, description=description)
                )

        error = False
        try:
            for item in stationery:
                item.add()

            db.session.commit()
        except Exception:
            error = True
            print(exc_info())

        if not error:
            return jsonify({"success": True, "data": len(stationery)})

    @app.route("/stationery/<int:item_id>", methods=["PUT"])
    def update_item(item_id):
        name = request.json.get("name", None)
        description = request.json.get("description", None)

        item = Stationery.query.get(item_id)

        if not item:
            abort(404)

        item.name = name
        item.description = description

        error = False
        try:
            new_item = item.update()
        except Exception:
            error = True
            print(exc_info())

        if not error:
            return jsonify({"success": True, "data": new_item.format_long()})

    @app.route("/stationery/<int:item_id>", methods=["DELETE"])
    def delete_item(item_id):
        item = Stationery.query.get(item_id)

        if not item:
            abort(404)

        error = False
        try:
            item.delete()
        except Exception:
            error = True
            print(exc_info())

        if not error:
            return jsonify({"success": True})
