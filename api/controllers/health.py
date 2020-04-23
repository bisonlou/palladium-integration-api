from flask import jsonify

def health_check(app):
    @app.route("/health")
    def get_health_check():
        return jsonify(
            {"success": True, "message": "healthy"}
        )
