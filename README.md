# Palladium Integration API

A Flask-based API for Palladium integration, featuring payroll journal generation and user management with password reset functionality.

## 🚀 Quick Start

### Automated Setup
```bash
# Clone the repository
git clone <repository-url>
cd palladium-integration-api

# Run the setup script
./setup.sh
```

### Manual Setup
1. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   python -m pip install -r requirements.txt
   ```

3. **Configure database:**
   ```bash
   # Update .env with PostgreSQL credentials
   alembic upgrade head  # Run migrations
   ```

4. **Start the server:**
   ```bash
   python app.py
   ```

## 📧 Password Reset Feature

This API includes a complete password reset system with:
- Secure token generation and email delivery
- HTML email templates
- Token expiration and validation
- Security best practices

### Endpoints:
- `POST /forgot-password` - Request password reset
- `POST /reset-password` - Reset password with token

For detailed setup and usage, see [PASSWORD_RESET_README.md](PASSWORD_RESET_README.md).

## ⚙️ Configuration

Key environment variables (see `.env.example`):

```bash
# Database
POSTGRES_DATABASE_URL=postgresql://user:pass@localhost:5432/db

# Email (for password reset)
SMTP_SERVER=smtp.gmail.com
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Application
SECRET=your-secret-key
FRONTEND_URL=http://localhost:3000
```

## 📁 Project Structure

```
palladium-integration-api/
├── api/
│   ├── controllers/          # API endpoints
│   ├── models/              # Database models  
│   ├── utils/               # Utilities (email, tokens)
│   └── database/            # Database configuration
├── migrations/              # Database migrations
├── tests/                   # Unit tests
├── .env.example            # Environment template
└── PASSWORD_RESET_README.md # Detailed password reset docs
```

## 🛠️ Features

- **Journal Generation**: Payroll journal file generation
- **User Management**: User registration and authentication
- **Password Reset**: Secure email-based password reset
- **Database Migrations**: Alembic for schema management
- **Testing**: Unit tests included
- **Docker Support**: Docker and docker-compose configuration
