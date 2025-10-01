from datetime import datetime, timedelta
from api.database import db


class PasswordResetToken(db.Model):
    __tablename__ = "password_reset_tokens"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    used = db.Column(db.Boolean, default=False)

    # Relationship to User
    user = db.relationship("User", backref="reset_tokens")

    def __init__(self, user_id, token, expires_at=None):
        self.user_id = user_id
        self.token = token
        if expires_at is None:
            # Token expires in 1 hour by default
            self.expires_at = datetime.utcnow() + timedelta(hours=1)
        else:
            self.expires_at = expires_at

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    def is_valid(self):
        return not self.used and not self.is_expired()

    def mark_as_used(self):
        self.used = True
        db.session.commit()

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.id

    @staticmethod
    def cleanup_expired_tokens():
        """Remove expired tokens from the database"""
        expired_tokens = PasswordResetToken.query.filter(
            PasswordResetToken.expires_at < datetime.utcnow()
        ).all()
        
        for token in expired_tokens:
            db.session.delete(token)
        
        db.session.commit()
        return len(expired_tokens)

    @staticmethod
    def find_valid_token(token_string):
        """Find a valid (not used, not expired) token"""
        token = PasswordResetToken.query.filter_by(token=token_string).first()
        
        if token and token.is_valid():
            return token
        
        return None