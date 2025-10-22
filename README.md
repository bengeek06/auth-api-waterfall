# PM Auth API

[![Tests](https://github.com/bengeek06/pm-auth-api/actions/workflows/python-app.yml/badge.svg)](https://github.com/bengeek06/pm-auth-api/actions)
[![License: AGPL v3 / Commercial](https://img.shields.io/badge/license-AGPLv3%20%2F%20Commercial-blue)](LICENCE.md)
[![OpenAPI Spec](https://img.shields.io/badge/OpenAPI-3.0-blue.svg)](openapi.yml)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/flask-%3E=2.0-green.svg)
![Coverage](https://img.shields.io/badge/coverage-pytest-green.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)


---

## Overview

**PM Auth API** is a RESTful authentication service for user login, logout, token verification, refresh, and configuration/version/health endpoints.  
It uses JWT for access tokens and supports secure cookie-based authentication.

---

## Project Structure

```
.
├── app
│   ├── config.py
│   ├── __init__.py
│   ├── logger.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── refresh_token.py
│   │   └── token_blacklist.py
│   ├── resources
│   │   ├── config.py
│   │   ├── health.py
│   │   ├── __init__.py
│   │   ├── login.py
│   │   ├── logout.py
│   │   ├── refresh.py
│   │   ├── verify.py
│   │   └── version.py
│   ├── routes.py
│   └── utils.py
├── CODE_OF_CONDUCT.md
├── COMMERCIAL-LICENCE.txt
├── Dockerfile
├── env.example
├── instance/
├── LICENCE.md
├── migrations/
├── openapi.yml
├── pytest.ini
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── run.py
├── tests/
├── wait-for-it.sh
└── wsgi.py
```

---

## Environments

The application supports multiple environments, each with its own configuration:

- **Development**: For local development. Debug mode enabled.
- **Testing**: For running automated tests. Uses a separate test database.
- **Staging**: For pre-production validation. Debug mode enabled, but production-like settings.
- **Production**: For live deployments. Debug mode disabled, secure settings.

Set the environment with the `FLASK_ENV` environment variable (`development`, `testing`, `staging`, `production`).  
Database URL and secrets are configured via environment variables (see `env.example`).

---

## Environment Variables

The service reads the following variables (see env.example):

| Variable              | Description |
|-----------------------|-------------|
| FLASK_ENV             | Environment (development, testing, staging, production) |
| LOG_LEVEL             | Logging level (DEBUG, INFO, etc.) |
| DATABASE_URL          | SQLAlchemy database URL |
| USER_SERVICE_URL      | External user service base URL (for credential verification) |
| INTERNAL_AUTH_TOKEN   | Internal shared secret for inter-service auth |
| JWT_SECRET            | Secret used to sign JWTs |

---

## Features

- User authentication with JWT access and refresh tokens
- Token revocation (blacklist)
- Token refresh endpoint
- Configuration and version endpoints
- Secure HttpOnly cookies for tokens
- OpenAPI 3.0 documentation

---

## Quickstart

### Requirements

- Python 3.11+
- pip

### Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

(For development tooling:)

```bash
pip install -r requirements-dev.txt
```

### Environment

Copy and edit the example environment file:

```bash
cp env.example .env.development # or .env.test
```

Set at least:

- `FLASK_ENV=development`
- `DATABASE_URL=sqlite:///pm-auth.db`
- `USER_SERVICE_URL=http://identity_service:5000`
- `INTERNAL_AUTH_TOKEN=your_secret`
- `JWT_SECRET=your_jwt_secret`

### Running

```bash
python run.py
```

Gunicorn (production-style):

```bash
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

---

## API Documentation

The OpenAPI specification is available in [openapi.yml](openapi.yml).  
You can visualize it with [Swagger Editor](https://editor.swagger.io/) or [Redoc](https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/bengeek06/pm-auth-api/refs/heads/guardian_staging/openapi.yml).


---

## Endpoints

| Method | Path      | Description                       |
|--------|-----------|-----------------------------------|
| POST   | /login    | User login, returns tokens        |
| POST   | /logout   | User logout, revokes tokens       |
| POST   | /refresh  | Refresh access token              |
| GET    | /verify   | Verify access token               |
| GET    | /config   | Get app configuration             |
| GET    | /version  | Get API version                   |
| GET    | /health   | Service health status (new)       |

/health returns a simple JSON status (extendable for DB checks later).

---

## Running Tests

```bash
pytest
```

(Uses FLASK_ENV=testing automatically via conftest.)

---

## Docker Usage

You can run the service using the production image (either locally built or from GHCR).

### Run with docker (production mode)

```bash
docker run -d \
  --name auth_service \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e LOG_LEVEL=INFO \
  -e DATABASE_URL=postgresql://user:pass@db:5432/auth_prod \
  -e USER_SERVICE_URL=http://users_service:5000 \
  -e INTERNAL_AUTH_TOKEN=change-me-internal \
  -e JWT_SECRET=change-me-jwt \
  ghcr.io/<owner>/<repo>:latest
```

If you built locally:
```bash
docker build -t auth-service:prod --target production .
docker run -d --name auth_service -p 5000:5000 -e FLASK_ENV=production auth-service:prod
```

Optional (supported by entrypoint if present):
- `WAIT_FOR_DB=true`
- `RUN_MIGRATIONS=true`

### docker-compose example

```yaml
version: "3.9"

services:
  auth_service:
    image: ghcr.io/<owner>/<repo>:latest
    container_name: auth_service
    restart: unless-stopped
    environment:
      FLASK_ENV: production
      LOG_LEVEL: INFO
      DATABASE_URL: postgresql://auth_user:auth_pass@db:5432/auth_db
      USER_SERVICE_URL: http://users_service:5000
      INTERNAL_AUTH_TOKEN: ${INTERNAL_AUTH_TOKEN:-change-me-internal}
      JWT_SECRET: ${JWT_SECRET:-change-me-jwt}
      WAIT_FOR_DB: "true"
      RUN_MIGRATIONS: "true"
    depends_on:
      - db
    ports:
      - "5000:5000"

  db:
    image: postgres:15-alpine
    container_name: auth_db
    restart: unless-stopped
    environment:
      POSTGRES_USER: auth_user
      POSTGRES_PASSWORD: auth_pass
      POSTGRES_DB: auth_db
    volumes:
      - auth_pg_data:/var/lib/postgresql/data

  # Optional example user service dependency
  users_service:
    image: ghcr.io/<owner>/<user-service-repo>:latest
    environment:
      FLASK_ENV: production
    restart: unless-stopped

volumes:
  auth_pg_data:
```

Create a `.env` file alongside docker-compose to override secrets:

```
INTERNAL_AUTH_TOKEN=super-secret-internal
JWT_SECRET=super-secret-jwt
```

Start:
```bash
docker compose up -d
```

### Health check

```bash
curl -s http://localhost:5000/health
```

---

## License

This project is dual-licensed:

- **Community version**: [GNU AGPLv3](https://www.gnu.org/licenses/agpl-3.0.html)
- **Commercial license**: See [LICENCE.md](LICENCE.md) and [COMMERCIAL-LICENCE.txt](COMMERCIAL-LICENCE.txt)

For commercial use or support, contact: **bengeek06@gmail.com**

---

## Contributing

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for guidelines.

---