# Password Reset Implementation

This document describes the real-world password reset functionality implemented in the Palladium Integration API.

## Features

- **Secure Token Generation**: Cryptographically secure tokens with timestamp components
- **Email Integration**: HTML and text email templates with professional styling  
- **Token Expiration**: Tokens automatically expire after 1 hour
- **Security Best Practices**: 
  - Tokens are single-use only
  - No email enumeration attacks (same response whether user exists or not)
  - Automatic cleanup of expired tokens
  - Password strength validation

## API Endpoints

### 1. Request Password Reset

**Endpoint**: `POST /forgot-password`

**Request Body**:
```json
{
  "email": "username"  // without @eprcug.org suffix
}
```

**Response** (Always returns 200 for security):
```json
{
  "success": true,
  "description": "If an account with that email exists, password reset instructions have been sent"
}
```

### 2. Reset Password with Token

**Endpoint**: `POST /reset-password`

**Request Body**:
```json
{
  "token": "secure-reset-token-from-email",
  "new_password": "newPassword123"
}
```

**Success Response**:
```json
{
  "success": true,
  "description": "Password has been successfully reset"
}
```

**Error Responses**:
```json
{
  "success": false,
  "description": "Invalid or expired token"
}
```

## Setup Instructions

### 1. Database Migration

Run the migration to create the password reset tokens table:

```bash
# Apply the migration
alembic upgrade head
```

### 2. Environment Variables

Configure the following environment variables for email functionality:

```bash
# SMTP Configuration
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USERNAME=your-email@gmail.com
export SMTP_PASSWORD=your-app-password

# Email Settings  
export FROM_EMAIL=noreply@eprcug.org
export FROM_NAME="Palladium Integration API"

# Frontend URL (for password reset links)
export FRONTEND_URL=http://localhost:3000

# Required for JWT (should already exist)
export SECRET=your-secret-key-here
```

### 3. Gmail Setup (Recommended)

For Gmail SMTP:

1. Enable 2-factor authentication on your Gmail account
2. Go to Google Account settings > Security > App passwords
3. Generate an app password for "Mail"
4. Use that app password as `SMTP_PASSWORD`

### 4. Frontend Integration

The password reset emails contain links to your frontend application. Ensure your frontend handles the `/reset-password?token=...` route.

## Security Features

### Token Security
- **Cryptographically secure**: Uses Python's `secrets` module
- **Time-limited**: 1-hour expiration with database enforcement
- **Single-use**: Tokens are marked as used after password reset
- **Format validation**: Tokens are validated before processing

### Email Security
- **No enumeration**: Same response whether user exists or not
- **Professional templates**: HTML and text versions included
- **Secure links**: Tokens embedded in secure URLs

### Database Security
- **Automatic cleanup**: Expired tokens are cleaned up automatically
- **Foreign key constraints**: Proper relationships to user table
- **Unique tokens**: Database-level uniqueness constraint

## File Structure

```
api/
├── models/
│   └── password_reset_token.py    # Database model for reset tokens
├── utils/
│   ├── email_service.py           # Email sending functionality
│   └── token_utils.py             # Secure token generation
└── controllers/
    └── users.py                   # Updated with reset endpoints
migrations/
└── versions/
    └── c2a4f5e6d7b8_*.py          # Database migration
```

## Error Handling

The implementation includes comprehensive error handling:

- **Invalid tokens**: Proper validation and error messages
- **Expired tokens**: Automatic detection and cleanup
- **Email failures**: Graceful handling without exposing errors
- **Database errors**: Transaction rollback and error recovery
- **Validation errors**: Password strength and format validation

## Testing

Test the endpoints using curl or your preferred API client:

```bash
# Request password reset
curl -X POST http://localhost:8080/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email": "testuser"}'

# Reset password (replace TOKEN with actual token from email)
curl -X POST http://localhost:8080/reset-password \
  -H "Content-Type: application/json" \
  -d '{"token": "TOKEN", "new_password": "newPassword123"}'
```

## Production Considerations

1. **Rate Limiting**: Consider adding rate limiting to prevent abuse
2. **Monitoring**: Log password reset attempts for security monitoring  
3. **Email Delivery**: Use a professional email service (SendGrid, AWS SES, etc.)
4. **HTTPS**: Ensure all password reset links use HTTPS in production
5. **Token Cleanup**: Consider adding a cron job to clean up expired tokens

## Troubleshooting

### Email Not Sending
- Check SMTP credentials and server settings
- Verify firewall allows SMTP connections
- Check application logs for detailed error messages

### Tokens Not Working  
- Verify database migration was applied
- Check token expiration times
- Ensure tokens haven't been used already

### Frontend Integration Issues
- Verify `FRONTEND_URL` environment variable
- Check that frontend properly handles the reset password route
- Ensure token is properly extracted from URL parameters