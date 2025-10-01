import os
import sys
import jwt
from flask import jsonify, abort, request
from werkzeug.security import generate_password_hash, check_password_hash
from api.models.user import User
from api.models.password_reset_token import PasswordResetToken
from api.utils.email_service import email_service
from api.utils.token_utils import generate_reset_token_with_timestamp, is_token_format_valid


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

    @app.route("/forgot-password", methods=["POST"])
    def forgot_password():
        email = request.json.get("email", None)
        
        if not email:
            return (
                jsonify(
                    {
                        "success": False,
                        "description": "Email is required",
                    }
                ),
                400,
            )
        
        # Add @eprcug.org suffix if not already present
        if "@" not in email:
            full_email = f"{email}@eprcug.org"
        else:
            full_email = email
        
        # Check if user exists with this email
        user = User.query.filter(User.email == full_email).first()
        
        if user is None:
            # For security, don't reveal that the email doesn't exist
            # Return success anyway to prevent email enumeration attacks
            return (
                jsonify(
                    {
                        "success": True,
                        "description": "If an account with that email exists, password reset instructions have been sent",
                    }
                ),
                200,
            )
        
        try:
            # Clean up any existing tokens for this user
            existing_tokens = PasswordResetToken.query.filter_by(user_id=user.id).all()
            for token in existing_tokens:
                token.delete()
            
            # Generate a new secure token
            reset_token, expires_at = generate_reset_token_with_timestamp()
            
            # Save token to database
            password_reset_token = PasswordResetToken(
                user_id=user.id,
                token=reset_token,
                expires_at=expires_at
            )
            password_reset_token.add()
            
            # Send password reset email
            user_name = f"{user.first_name} {user.last_name}".strip()
            email_sent = email_service.send_password_reset_email(
                to_email=user.email,
                reset_token=reset_token,
                user_name=user_name if user_name else None
            )
            
            if not email_sent:
                # Log the error but don't expose it to the user
                print(f"Failed to send password reset email to {user.email}")
            
            return (
                jsonify(
                    {
                        "success": True,
                        "description": "If an account with that email exists, password reset instructions have been sent",
                    }
                ),
                200,
            )
            
        except Exception as e:
            print(f"Error in forgot_password: {str(e)}")
            return (
                jsonify(
                    {
                        "success": False,
                        "description": "An error occurred while processing your request. Please try again later.",
                    }
                ),
                500,
            )

    @app.route("/reset-password", methods=["POST"])
    def reset_password():
        token = request.json.get("token", None)
        new_password = request.json.get("new_password", None)
        
        if not token or not new_password:
            return (
                jsonify(
                    {
                        "success": False,
                        "description": "Token and new password are required",
                    }
                ),
                400,
            )
        
        # Validate token format
        if not is_token_format_valid(token):
            return (
                jsonify(
                    {
                        "success": False,
                        "description": "Invalid token format",
                    }
                ),
                400,
            )
        
        # Validate password strength (basic validation)
        if len(new_password) < 8:
            return (
                jsonify(
                    {
                        "success": False,
                        "description": "Password must be at least 8 characters long",
                    }
                ),
                400,
            )
        
        try:
            # Find and validate the reset token
            reset_token = PasswordResetToken.find_valid_token(token)
            
            if not reset_token:
                return (
                    jsonify(
                        {
                            "success": False,
                            "description": "Invalid or expired token",
                        }
                    ),
                    400,
                )
            
            # Get the user
            user = User.query.get(reset_token.user_id)
            if not user:
                return (
                    jsonify(
                        {
                            "success": False,
                            "description": "User not found",
                        }
                    ),
                    404,
                )
            
            # Update user's password
            hashed_password = generate_password_hash(new_password, method="sha256")
            user.password = hashed_password
            
            # Mark token as used
            reset_token.mark_as_used()
            
            # Clean up any other tokens for this user
            other_tokens = PasswordResetToken.query.filter(
                PasswordResetToken.user_id == user.id,
                PasswordResetToken.id != reset_token.id
            ).all()
            
            for other_token in other_tokens:
                other_token.delete()
            
            # Commit the password change
            from api.database import db
            db.session.commit()
            
            return (
                jsonify(
                    {
                        "success": True,
                        "description": "Password has been successfully reset",
                    }
                ),
                200,
            )
            
        except Exception as e:
            print(f"Error in reset_password: {str(e)}")
            from api.database import db
            db.session.rollback()
            return (
                jsonify(
                    {
                        "success": False,
                        "description": "An error occurred while resetting your password. Please try again later.",
                    }
                ),
                500,
            )

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
