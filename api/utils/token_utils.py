import secrets
import string
from datetime import datetime, timedelta


def generate_reset_token(length=32):
    """
    Generate a cryptographically secure random token for password reset.
    
    Args:
        length (int): Length of the token (default: 32)
        
    Returns:
        str: A secure random token
    """
    # Use URL-safe characters (letters, digits, - and _)
    alphabet = string.ascii_letters + string.digits + '-_'
    token = ''.join(secrets.choice(alphabet) for _ in range(length))
    return token


def generate_secure_token_hex(length=32):
    """
    Generate a cryptographically secure random token using hexadecimal.
    
    Args:
        length (int): Number of bytes (resulting hex will be 2x this length)
        
    Returns:
        str: A secure random hex token
    """
    return secrets.token_hex(length)


def generate_reset_token_with_timestamp():
    """
    Generate a reset token with embedded timestamp for additional security.
    
    Returns:
        tuple: (token, expires_at) where expires_at is datetime object
    """
    # Generate base token
    base_token = generate_reset_token(24)
    
    # Add timestamp component
    timestamp = str(int(datetime.utcnow().timestamp()))
    
    # Combine with additional random component
    random_suffix = generate_reset_token(8)
    
    token = f"{base_token}-{timestamp}-{random_suffix}"
    expires_at = datetime.utcnow() + timedelta(hours=1)
    
    return token, expires_at


def is_token_format_valid(token):
    """
    Basic validation of token format.
    
    Args:
        token (str): Token to validate
        
    Returns:
        bool: True if format appears valid
    """
    if not token or not isinstance(token, str):
        return False
    
    # Check if token contains only allowed characters
    allowed_chars = string.ascii_letters + string.digits + '-_'
    if not all(c in allowed_chars for c in token):
        return False
    
    # Check reasonable length (minimum 16, maximum 100 characters)
    if len(token) < 16 or len(token) > 100:
        return False
    
    return True