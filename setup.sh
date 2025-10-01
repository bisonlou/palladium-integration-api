#!/bin/bash

# =======================================================================
# Palladium Integration API - Setup Script
# =======================================================================
# This script helps set up the development environment

set -e  # Exit on any error

echo "🚀 Setting up Palladium Integration API..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file. Please edit it with your configuration."
    echo "   Important: Update database credentials, email settings, and SECRET key!"
else
    echo "✅ .env file already exists"
fi

# Check if Python virtual environment exists
if [ ! -d "venv" ] && [ ! -d "env" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Activated virtual environment (venv)"
elif [ -d "env" ]; then
    source env/bin/activate
    echo "✅ Activated virtual environment (env)"
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Check PostgreSQL connection
echo "🗄️  Checking database configuration..."
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL client found"
    echo "💡 Make sure your PostgreSQL server is running and configured in .env"
else
    echo "⚠️  PostgreSQL client not found. Please install PostgreSQL:"
    echo "   macOS: brew install postgresql"
    echo "   Ubuntu: sudo apt install postgresql postgresql-contrib"
fi

# Run database migrations
echo "🔄 Running database migrations..."
if [ -f "migrations/alembic.ini" ]; then
    # Check if alembic command works
    if python -c "import alembic" &> /dev/null; then
        echo "Running: alembic upgrade head"
        alembic upgrade head
        echo "✅ Database migrations completed"
    else
        echo "⚠️  Alembic not properly installed. Run manually: alembic upgrade head"
    fi
else
    echo "⚠️  No migrations found. Database schema may need to be created manually."
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your configuration:"
echo "   - Database credentials (POSTGRES_* variables)"
echo "   - Email settings (SMTP_* variables)"  
echo "   - Update SECRET key for production"
echo ""
echo "2. Start the development server:"
echo "   python app.py"
echo ""
echo "3. Test the password reset endpoints:"
echo "   POST /forgot-password"
echo "   POST /reset-password"
echo ""
echo "📚 For detailed setup instructions, see PASSWORD_RESET_README.md"
echo ""
echo "🔧 Troubleshooting:"
echo "   - Ensure PostgreSQL is running on localhost:5432"
echo "   - Check .env file for correct database URL"
echo "   - For Gmail: use App Password, not regular password"
echo "   - Frontend URL should match your React/frontend app"