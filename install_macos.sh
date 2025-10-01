#!/bin/bash

# =======================================================================
# Palladium Integration API - macOS Installation Fix
# =======================================================================
# This script handles common installation issues on macOS

set -e  # Exit on any error

echo "🔧 Fixing installation issues for macOS..."

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "This script is designed for macOS. For other systems, see README.md"
    exit 1
fi

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "📦 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew is installed"
fi

# Install PostgreSQL if not present
if ! command -v psql &> /dev/null; then
    echo "🗄️ Installing PostgreSQL..."
    brew install postgresql
    brew services start postgresql
    echo "✅ PostgreSQL installed and started"
else
    echo "✅ PostgreSQL is already installed"
fi

# Install Python dependencies that might be needed for compilation
echo "🔧 Installing system dependencies..."
brew install libpq
export PATH="/opt/homebrew/bin:$PATH"
export LDFLAGS="-L/opt/homebrew/lib"
export CPPFLAGS="-I/opt/homebrew/include"

# Create or activate virtual environment
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip first
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install wheel and setuptools
echo "📦 Installing build tools..."
pip install wheel setuptools

# Try to install psycopg2-binary specifically first
echo "📦 Installing psycopg2-binary..."
pip install psycopg2-binary==2.8.4

# Install the rest of the requirements
echo "📦 Installing remaining requirements..."
pip install -r requirements.txt

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "🚀 Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Configure .env file if not done: cp .env.example .env"
echo "3. Run verification: python verify_setup.py"
echo "4. Start server: python app.py"