#!/usr/bin/env python3
"""
Environment Configuration Verification Script
This script checks if all required environment variables are properly configured.
"""

import os
import sys
from dotenv import load_dotenv

def check_env_vars():
    """Check if all required environment variables are set"""
    
    # Load .env file
    load_dotenv()
    
    required_vars = [
        'FLASK_ENV',
        'SECRET',
        'POSTGRES_DATABASE_URL',
    ]
    
    optional_vars = [
        'SMTP_SERVER',
        'SMTP_USERNAME', 
        'SMTP_PASSWORD',
        'FROM_EMAIL',
        'FRONTEND_URL',
    ]
    
    print("🔍 Checking environment configuration...\n")
    
    # Check required variables
    missing_required = []
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # Mask sensitive values
            if 'SECRET' in var or 'PASSWORD' in var:
                display_value = '*' * len(value)
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NOT SET")
            missing_required.append(var)
    
    print()
    
    # Check optional variables (for password reset functionality)
    missing_optional = []
    for var in optional_vars:
        value = os.environ.get(var)
        if value:
            # Mask sensitive values
            if 'PASSWORD' in var or 'SECRET' in var:
                display_value = '*' * len(value)
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"⚠️  {var}: NOT SET (optional - needed for password reset)")
            missing_optional.append(var)
    
    print()
    
    # Summary
    if missing_required:
        print("❌ CONFIGURATION INCOMPLETE")
        print(f"Missing required variables: {', '.join(missing_required)}")
        print("Please update your .env file with the missing values.")
        return False
    else:
        print("✅ BASIC CONFIGURATION COMPLETE")
        if missing_optional:
            print(f"Optional variables not set: {', '.join(missing_optional)}")
            print("Password reset functionality will not work without email configuration.")
        else:
            print("All configuration variables are set!")
        return True

def test_database_connection():
    """Test database connection"""
    print("\n🗄️  Testing database connection...")
    
    try:
        import psycopg2
        from urllib.parse import urlparse
        
        db_url = os.environ.get('POSTGRES_DATABASE_URL')
        if not db_url:
            print("❌ No database URL configured")
            return False
        
        # Parse database URL
        parsed = urlparse(db_url)
        
        # Test connection
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path[1:],  # Remove leading '/'
            user=parsed.username,
            password=parsed.password
        )
        conn.close()
        
        print("✅ Database connection successful")
        return True
        
    except ImportError:
        print("⚠️  psycopg2 not installed - skipping database test")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def test_email_config():
    """Test email configuration"""
    print("\n📧 Testing email configuration...")
    
    required_email_vars = ['SMTP_SERVER', 'SMTP_USERNAME', 'SMTP_PASSWORD']
    
    for var in required_email_vars:
        if not os.environ.get(var):
            print(f"⚠️  Email not configured - missing {var}")
            return False
    
    print("✅ Email configuration looks good")
    print("💡 To test email sending, try the /forgot-password endpoint")
    return True

def main():
    """Main verification function"""
    print("=" * 60)
    print("Palladium Integration API - Environment Verification")
    print("=" * 60)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please copy .env.example to .env and configure it.")
        sys.exit(1)
    
    # Run checks
    config_ok = check_env_vars()
    db_ok = test_database_connection() 
    email_ok = test_email_config()
    
    print("\n" + "=" * 60)
    
    if config_ok and db_ok:
        print("🎉 Environment setup looks good!")
        print("\n🚀 You can now start the server with: python app.py")
        
        if not email_ok:
            print("\n📧 Note: Configure email settings to enable password reset")
            
    else:
        print("❌ Environment setup needs attention")
        print("\n📚 See README.md and PASSWORD_RESET_README.md for setup help")
        sys.exit(1)

if __name__ == '__main__':
    main()