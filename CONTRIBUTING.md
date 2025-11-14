# Contributing to Auth Service

Thank you for your interest in contributing to the **PM Auth API** service!

> **Note**: This service is part of the larger [Waterfall](../../README.md) project. For the overall development workflow, branch strategy, and contribution guidelines, please refer to the [main CONTRIBUTING.md](../../CONTRIBUTING.md) in the root repository.

## Table of Contents

- [Service Overview](#service-overview)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [API Development](#api-development)
- [Database Migrations](#database-migrations)
- [Common Tasks](#common-tasks)

## Service Overview

The **Auth Service** handles user authentication and authorization for the Waterfall platform:

- **Technology Stack**: Python 3.13+, Flask 3.1+, SQLAlchemy, PostgreSQL
- **Port**: 5001 (containerized) / 5000 (standalone)
- **Responsibilities**:
  - User login/logout
  - JWT token generation and validation
  - Token refresh mechanism
  - Token blacklisting for logout
  - Health and configuration endpoints

**Key Dependencies:**
- Flask 3.1+ for REST API
- SQLAlchemy for ORM
- PyJWT for token management
- Werkzeug for password hashing
- Gunicorn for production WSGI server

## Development Setup

### Prerequisites

- Python 3.13+
- PostgreSQL 16+ (or use Docker)
- pip and virtualenv

### Local Setup

```bash
# Navigate to service directory
cd services/auth_service

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install development tools
pip install -r requirements-dev.txt

# Copy environment configuration
cp env.example .env.development

# Configure environment variables
# Edit .env.development with your local settings
```

### Environment Configuration

Create `.env.development` with the following variables:

```bash
# Flask environment
FLASK_ENV=development
LOG_LEVEL=DEBUG

# Database
DATABASE_URL=postgresql://auth_user:auth_pass@localhost:5432/auth_dev

# External services
USER_SERVICE_URL=http://localhost:5002
INTERNAL_AUTH_TOKEN=dev-internal-secret

# Security
JWT_SECRET=dev-jwt-secret-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=900  # 15 minutes
JWT_REFRESH_TOKEN_EXPIRES=604800  # 7 days
```

### Database Setup

```bash
# Create database (if using local PostgreSQL)
createdb auth_dev

# Run migrations
flask db upgrade

# Or use Docker for PostgreSQL
docker run -d \
  --name auth_db_dev \
  -e POSTGRES_USER=auth_user \
  -e POSTGRES_PASSWORD=auth_pass \
  -e POSTGRES_DB=auth_dev \
  -p 5432:5432 \
  postgres:16-alpine
```

### Running the Service

```bash
# Development mode with auto-reload
python run.py

# Or with Flask CLI
export FLASK_APP=wsgi:app
flask run --port=5000

# Production-style with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

The service will be available at `http://localhost:5000`

## Coding Standards

### Python Style Guide

This service follows **PEP 8** style guidelines with the following tools:

**Black** - Code formatter:
```bash
# Format all code
black app/ tests/

# Check without modifying
black --check app/ tests/
```

**Pylint** - Linter:
```bash
# Check code quality
pylint app/ tests/

# Configuration in .pylintrc or pyproject.toml
```

**isort** - Import sorting:
```bash
# Sort imports
isort app/ tests/

# Check only
isort --check-only app/ tests/
```

### Code Conventions

**File Structure:**
```python
# Standard library imports
import os
from datetime import datetime

# Third-party imports
from flask import Blueprint, request, jsonify
from sqlalchemy import Column, Integer, String

# Local imports
from app.models import User
from app.utils import generate_token
```

**Type Hints** (Python 3.13+):
```python
from typing import Optional, Dict, Any

def create_token(user_id: int, expires_delta: Optional[int] = None) -> str:
    """Generate JWT access token.
    
    Args:
        user_id: The user's database ID
        expires_delta: Token expiration time in seconds (optional)
    
    Returns:
        Encoded JWT token as string
    
    Raises:
        ValueError: If user_id is invalid
    """
    # Implementation
    pass
```

**Docstrings** (Google style):
```python
class RefreshToken(db.Model):
    """Refresh token model for persistent token storage.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to user table
        token: Hashed refresh token
        created_at: Token creation timestamp
        expires_at: Token expiration timestamp
    """
    pass
```

**Constants and Configuration:**
```python
# Use uppercase for constants
DEFAULT_TOKEN_EXPIRY = 900
MAX_LOGIN_ATTEMPTS = 5

# Config classes in app/config.py
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
```

### Error Handling

```python
from flask import jsonify
from app.logger import logger

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        # Process login
        return jsonify({"status": "success"}), 200
    except ValueError as e:
        logger.warning(f"Invalid login data: {e}")
        return jsonify({"error": "Invalid credentials"}), 400
    except Exception as e:
        logger.error(f"Login error: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_login.py

# Run with coverage
pytest --cov=app --cov-report=html

# Run with markers
pytest -m "unit"  # Only unit tests
pytest -m "integration"  # Only integration tests
```

### Test Structure

```python
import pytest
from app import create_app
from app.models import db

class TestLoginEndpoint:
    """Test suite for login endpoint."""
    
    @pytest.fixture(autouse=True)
    def setup(self, client):
        """Setup for each test."""
        # Setup code
        yield
        # Teardown code
    
    def test_successful_login(self, client):
        """Test successful user login."""
        response = client.post('/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        assert 'access_token' in response.json
        assert response.json['status'] == 'success'
    
    def test_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post('/login', json={
            'email': 'test@example.com',
            'password': 'wrong_password'
        })
        
        assert response.status_code == 401
        assert 'error' in response.json
```

### Test Coverage Requirements

- **Minimum coverage**: 80% for new code
- **Critical paths**: Login, logout, token validation require 100% coverage
- **Focus areas**: Authentication logic, token generation, error handling

### Testing Best Practices

1. **Use fixtures** for common setup (database, client, test data)
2. **Test one thing** per test function
3. **Use descriptive names** that explain what is being tested
4. **Mock external services** (User Service calls)
5. **Clean up** after tests (use fixtures with yield)

## API Development

### Adding a New Endpoint

1. **Create resource file** in `app/resources/`:

```python
# app/resources/my_endpoint.py
from flask import Blueprint, request, jsonify
from app.logger import logger

my_endpoint_bp = Blueprint('my_endpoint', __name__)

@my_endpoint_bp.route('/my-endpoint', methods=['POST'])
def handle_my_endpoint():
    """Handle my new endpoint.
    
    Request Body:
        {
            "field1": "value1",
            "field2": "value2"
        }
    
    Returns:
        JSON response with status and data
    """
    try:
        data = request.get_json()
        # Process request
        return jsonify({"status": "success", "data": {}}), 200
    except Exception as e:
        logger.error(f"Error in my_endpoint: {e}")
        return jsonify({"error": "Internal error"}), 500
```

2. **Register blueprint** in `app/routes.py`:

```python
from app.resources.my_endpoint import my_endpoint_bp

def register_routes(app):
    app.register_blueprint(my_endpoint_bp)
    # ... other blueprints
```

3. **Add tests** in `tests/`:

```python
# tests/test_my_endpoint.py
def test_my_endpoint_success(client):
    response = client.post('/my-endpoint', json={
        "field1": "value1",
        "field2": "value2"
    })
    assert response.status_code == 200
```

4. **Update OpenAPI spec** in `openapi.yml`:

```yaml
paths:
  /my-endpoint:
    post:
      summary: My new endpoint
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                field1:
                  type: string
      responses:
        200:
          description: Success
```

## Database Migrations

### Creating Migrations

```bash
# Auto-generate migration from model changes
flask db migrate -m "Add new field to refresh_token table"

# Review the generated migration in migrations/versions/

# Apply migration
flask db upgrade

# Rollback if needed
flask db downgrade
```

### Manual Migrations

```python
# migrations/versions/xxx_add_new_field.py
def upgrade():
    op.add_column('refresh_token', 
        sa.Column('new_field', sa.String(255), nullable=True)
    )

def downgrade():
    op.drop_column('refresh_token', 'new_field')
```

### Migration Best Practices

1. **Always review** auto-generated migrations
2. **Test migrations** on development database first
3. **Provide downgrade** path for rollback
4. **Keep migrations small** and focused
5. **Never edit** applied migrations, create new ones

## Common Tasks

### Adding a New Model

```python
# app/models/my_model.py
from app.models import db
from datetime import datetime

class MyModel(db.Model):
    """Description of the model."""
    
    __tablename__ = 'my_table'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MyModel {self.name}>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }
```

### Updating Dependencies

```bash
# Update a specific package
pip install --upgrade flask

# Update requirements.txt
pip freeze > requirements.txt

# Or use pip-tools for better control
pip-compile requirements.in
pip-sync requirements.txt
```

### Debugging

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with debugger
python -m pdb run.py

# Or use Flask debug mode
export FLASK_ENV=development
python run.py
```

### Code Formatting

```bash
# Format everything before committing
black app/ tests/
isort app/ tests/
pylint app/ tests/

# Or use pre-commit hooks (if configured)
pre-commit run --all-files
```

## Service-Specific Guidelines

### Security Considerations

1. **Never log** sensitive data (passwords, tokens)
2. **Always hash** passwords with Werkzeug
3. **Validate input** on all endpoints
4. **Use environment variables** for secrets
5. **Implement rate limiting** for login attempts

### Token Management

1. **Short-lived access tokens** (15 minutes default)
2. **Long-lived refresh tokens** (7 days default)
3. **Blacklist tokens** on logout
4. **Rotate refresh tokens** on use
5. **Clean up expired tokens** periodically

### Integration with Other Services

This service communicates with:
- **Identity Service** (port 5002): User credential verification
- **Guardian Service** (port 5003): Permission checks (future)

Use `INTERNAL_AUTH_TOKEN` for inter-service authentication.

## Getting Help

- **Main Project**: See [root CONTRIBUTING.md](../../CONTRIBUTING.md)
- **Issues**: Use GitHub issues with `service:auth` label
- **Code of Conduct**: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- **Documentation**: [README.md](README.md)
- **OpenAPI Spec**: [openapi.yml](openapi.yml)

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)

---

**Remember**: Always refer to the [main CONTRIBUTING.md](../../CONTRIBUTING.md) for branch strategy, commit conventions, and pull request process!
