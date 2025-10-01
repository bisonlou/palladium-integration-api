#!/usr/bin/env python3
"""
Database Migration Script
Run this script to create/update database tables
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_migrations():
    """Run database migrations"""
    try:
        # Import Flask app and database
        from api import app
        from api.database import db
        
        with app.app_context():
            print("🗄️  Creating database tables...")
            
            # Create all tables
            db.create_all()
            
            print("✅ Database tables created successfully!")
            print("📋 Tables created:")
            
            # List all tables
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            for table in tables:
                print(f"   - {table}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creating database tables: {str(e)}")
        return False

def check_database_connection():
    """Check if database connection is working"""
    try:
        from api import app
        from api.database import db
        
        with app.app_context():
            # Try to execute a simple query
            result = db.engine.execute("SELECT 1")
            result.fetchone()
            print("✅ Database connection successful")
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        print("💡 Make sure PostgreSQL is running and .env is configured correctly")
        return False

def main():
    """Main migration function"""
    print("=" * 60)
    print("Palladium Integration API - Database Migration")
    print("=" * 60)
    
    # Check database connection first
    if not check_database_connection():
        print("\n🛠️  Database connection troubleshooting:")
        print("1. Ensure PostgreSQL is running")
        print("2. Check POSTGRES_DATABASE_URL in .env file")
        print("3. Verify database credentials")
        print("4. Create database if it doesn't exist:")
        print("   createdb eprc")
        return 1
    
    # Run migrations
    if run_migrations():
        print("\n🎉 Database migration completed successfully!")
        print("\n🚀 You can now start the server with: python app.py")
        return 0
    else:
        print("\n❌ Database migration failed")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)