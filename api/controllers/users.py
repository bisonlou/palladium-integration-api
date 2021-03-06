import os
import sys
import jwt
from flask import jsonify, abort, request
from werkzeug.security import generate_password_hash, check_password_hash
from api.models.user import User


def user_module(app):
    @app.route("/users")
    def get_users():
        users = User.query.all()

        return jsonify(
            {"success": True, "data": [user.format_long() for user in users]}
        )

    @app.route("/users/<int:user_id>")
    def get_user(user_id):
        user = User.query.get(user_id)

        if not user:
            abort(404)

        return jsonify({"success": True, "data": user.format_long()})

    @app.route("/users", methods=["POST"])
    def post_user():
        email = request.json.get("email", None)
        first_name = request.json.get("first_name", None)
        middle_name = request.json.get("middle_name", None)
        last_name = request.json.get("last_name", None)
        password = request.json.get("password", None)

        # errors = validate_user(data)
        # if errors:
        #     return jsonify({'status': 400, 'errors': errors}), 400

        user = User.query.filter(User.email == email).first()
        if user:
            return (
                jsonify(
                    {
                        "success": False,
                        "description": "User with that email already registered",
                    }
                ),
                422,
            )

        hashed_password = generate_password_hash(password, method="sha256")

        error = False
        try:
            new_user = User(
                email=email,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                password=hashed_password,
            )

            user = User.add(new_user)
        except Exception:
            print(sys.exc_info())
            error = True

        if not error:
            token = jwt.encode(
                {"id": user.id}, os.environ.get("SECRET"), algorithm="HS256"
            )

            return (
                jsonify(
                    {
                        "success": True,
                        "access_token": token.decode("utf-8"),
                        "user": user.format_long(),
                    }
                ),
                200,
            )

        abort(422)

    @app.route("/login", methods=["POST"])
    def login():
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        user = User.query.filter(User.email == email).first()

        if user is None:
            abort(401)

        if check_password_hash(user.password, password):
            token = jwt.encode(
                {"id": user.id}, os.environ.get("SECRET"), algorithm="HS256"
            )

            return (
                jsonify(
                    {
                        "success": True,
                        "access_token": token.decode("utf-8"),
                        "user": user.format_long(),
                    }
                ),
                200,
            )

        abort(401)

    @app.route("/users", methods=["DELETE"])
    def delete():
        email = request.json.get("email", None)

        user = User.query.filter(User.email == email).first()

        if user is None:
            abort(404)

        error = False
        deleted_user_id = 0
        try:
            deleted_user_id = user.delete()
        except Exception:
            error = True
            print(sys.exc_info())

        if not error:
            return (
                jsonify(
                    {
                        "success": True,
                        "user_id": deleted_user_id,
                        "message": "user succesfully deleted",
                    }
                ),
                200,
            )

        abort(422)
