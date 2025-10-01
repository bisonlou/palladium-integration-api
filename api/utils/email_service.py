import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app


class EmailService:
    def __init__(self):
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', 587))
        self.smtp_username = os.environ.get('SMTP_USERNAME')
        self.smtp_password = os.environ.get('SMTP_PASSWORD') 
        self.from_email = os.environ.get('FROM_EMAIL', self.smtp_username)
        self.from_name = os.environ.get('FROM_NAME', 'Palladium Integration API')

    def send_password_reset_email(self, to_email, reset_token, user_name=None):
        """Send password reset email with reset token"""
        try:
            # Create reset link - you'll need to replace this with your frontend URL
            base_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
            reset_link = f"{base_url}/reset-password?token={reset_token}"
            
            subject = "Password Reset Request - Palladium Integration"
            
            # Create HTML email content
            html_content = self._get_password_reset_html_template(
                user_name or to_email.split('@')[0], 
                reset_link
            )
            
            # Create text version as fallback
            text_content = f"""
Hello {user_name or 'User'},

You have requested to reset your password for your Palladium Integration account.

Click the link below to reset your password:
{reset_link}

This link will expire in 1 hour for security reasons.

If you did not request this password reset, please ignore this email.

Best regards,
Palladium Integration Team
            """.strip()
            
            return self._send_email(to_email, subject, text_content, html_content)
            
        except Exception as e:
            current_app.logger.error(f"Failed to send password reset email to {to_email}: {str(e)}")
            return False

    def _send_email(self, to_email, subject, text_content, html_content=None):
        """Send email using SMTP"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            # Add text part
            text_part = MIMEText(text_content, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_content:
                html_part = MIMEText(html_content, 'html')
                msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            current_app.logger.error(f"SMTP error: {str(e)}")
            return False

    def _get_password_reset_html_template(self, user_name, reset_link):
        """Get HTML template for password reset email"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #007bff;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }}
        .content {{
            background-color: #f8f9fa;
            padding: 30px;
            border-radius: 0 0 5px 5px;
        }}
        .reset-button {{
            display: inline-block;
            background-color: #28a745;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
            font-weight: bold;
        }}
        .warning {{
            background-color: #fff3cd;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border: 1px solid #ffeaa7;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            font-size: 12px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Password Reset Request</h1>
    </div>
    
    <div class="content">
        <p>Hello <strong>{user_name}</strong>,</p>
        
        <p>You have requested to reset your password for your Palladium Integration account.</p>
        
        <p>Click the button below to reset your password:</p>
        
        <a href="{reset_link}" class="reset-button">Reset Password</a>
        
        <div class="warning">
            <strong>Important:</strong> This link will expire in 1 hour for security reasons.
        </div>
        
        <p>If you did not request this password reset, please ignore this email. Your password will remain unchanged.</p>
        
        <p>If you're having trouble clicking the button above, copy and paste the following URL into your web browser:</p>
        <p style="word-break: break-all; color: #007bff;">{reset_link}</p>
    </div>
    
    <div class="footer">
        <p>Best regards,<br>Palladium Integration Team</p>
    </div>
</body>
</html>
        """.strip()


# Create a singleton instance
email_service = EmailService()