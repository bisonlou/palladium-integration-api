from flask import abort, jsonify


def errorhandler(app):
    @app.errorhandler(404)
    def resource_not_found(error):
        return (
            jsonify(
                {
                    "success": False,
                    "message": "resource not found",
                    "error": 404,
                    "description": error.description,
                }
            ),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {
                    "success": False,
                    "message": "request unprocessable",
                    "error": 422,
                    "description": error.description,
                }
            ),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {
                    "success": False,
                    "message": "bad request",
                    "error": 400,
                    "description": error.description,
                }
            ),
            400,
        )

    @app.errorhandler(401)
    def unauthorized(error):
        return (
            jsonify(
                {
                    "success": False,
                    "message": "unauthorized",
                    "error": 401,
                    "description": error.description,
                }
            ),
            401,
        )

    @app.errorhandler(403)
    def permission_denied(error):
        return (
            jsonify(
                {
                    "success": False,
                    "message": "permission denied",
                    "error": 403,
                    "description": error.description,
                }
            ),
            403,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify(
                {
                    "success": False,
                    "message": "method not allowed",
                    "error": 405,
                    "description": error.description,
                }
            ),
            405,
        )
