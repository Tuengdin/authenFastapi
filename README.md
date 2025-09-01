# Authentication Microservice (FastAPI + SQLite)

Production-grade authentication / user management microservice using FastAPI and SQLite (can be swapped for Postgres).

## Features

- User registration with email verification token
- Secure password hashing (bcrypt via passlib)
- JWT access + refresh tokens (configurable lifetimes)
- Token revocation (refresh token rotation + blacklist table)
- Dependency-injected settings & DB session
- Alembic migrations scaffold
- Pydantic v2 models
- Basic rate limiting hook placeholder
- Structured logging
- Test suite with pytest & httpx AsyncClient
- **User roles:**

### **User Roles & Permissions**

1. **guest (Default Role)**:

   - **Permissions**:
     - Automatically assigned upon registration.
     - Can access public resources (e.g., public articles, homepage, open APIs).
   - **Limitations**:
     - Cannot perform authenticated user actions beyond basic registration / login.
     - Cannot access user-specific restricted content or administrative sections.

2. **member**:

   - **Permissions**:
     - Access member-designated areas (dashboard, profile, protected content).
     - Access enrolled courses.
     - Take exams and submit assignments.
     - View own learning results.
     - Update own profile and settings (email, password).
   - **Limitations**:
     - Cannot assign or modify roles for other users.
     - Cannot access administrative sections or system-wide settings.
     - Cannot create or edit courses.
     - Cannot manage other users.

3. **admin**:

   - **Permissions**:
     - Define which sections are accessible to members.
     - Manage user data within permitted scope (view, edit, delete non-admin users).
     - Assign or revoke roles for member users (not admin or superadmin).
     - Create and manage courses.
     - Review student performance.
     - View and manage user data (create, update, delete roles where allowed).
     - Configure LMS settings (notification emails, storage management).

# Authentication Microservice (FastAPI + SQLite)

Production-grade authentication / user management microservice using FastAPI and SQLite (easily swappable for Postgres).

## Features

- User registration
- Secure password hashing (bcrypt / passlib)
- JWT access + refresh tokens
- Token blacklist placeholder (refresh rotation foundation)
- Dependency-injected settings & async DB session
- Alembic-ready structure
- Pydantic v2 models
- Structured logging placeholder
- Basic test suite (pytest + httpx AsyncClient)
- Role-based access control (guest, member, admin, superadmin)

### Roles Summary

| Capability / Action                    | guest | member | admin | superadmin |
| -------------------------------------- | :---: | :----: | :---: | :--------: |
| Register / Authenticate                |  ✔\*  |   ✔    |   ✔   |     ✔      |
| Access public content                  |   ✔   |   ✔    |   ✔   |     ✔      |
| Access enrolled course content         |   ✖   |   ✔    |   ✔   |     ✔      |
| Submit assignments / take exams        |   ✖   |   ✔    |   ✔   |     ✔      |
| View own learning results              |   ✖   |   ✔    |   ✔   |     ✔      |
| Create / edit courses                  |   ✖   |   ✖    |   ✔   |     ✔      |
| Manage course enrollment               |   ✖   |   ✖    |   ✔   |     ✔      |
| View any user profile                  |   ✖   |   ✖    |   ✔   |     ✔      |
| Edit / delete users (non-admin)        |   ✖   |   ✖    |   ✔   |     ✔      |
| Assign/revoke member roles             |   ✖   |   ✖    |   ✔   |     ✔      |
| Assign/revoke admin / superadmin roles |   ✖   |   ✖    |   ✖   |     ✔      |
| Configure system-wide settings         |   ✖   |   ✖    |   ✖   |     ✔      |

\*guest can register and access limited authenticated endpoints.

## Quickstart

```bash
python -m venv venv
source venv/Scripts/activate  # Windows (Git Bash)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Tables auto-create on startup in dev/test via lifespan; use Alembic for production.

## Environment Variables (.env)

```
APP_NAME=auth-service
API_V1_PREFIX=/api/v1
SECRET_KEY=change_me
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_MINUTES=43200  # 30 days
ALGORITHM=HS256
DATABASE_URL=sqlite+aiosqlite:///./auth.db
LOG_LEVEL=INFO
```

## Testing

```bash
pytest -q
```

Current test: basic register + login (`tests/test_auth.py`). Add more for roles, refresh logic, permission denial.

## Project Layout

```
app/
├── main.py               # FastAPI app + lifespan (auto create tables dev/test)
├── core/
│   ├── config.py         # Settings
│   ├── security.py       # JWT / hashing utilities
│   └── logging_config.py # Logging setup
├── db/
│   ├── base.py           # SQLAlchemy Base
│   └── session.py        # Async engine/session
├── models/
│   ├── user.py           # User + roles
│   └── token_blacklist.py# Token blacklist placeholder
├── schemas/
│   ├── user.py           # User schemas
│   └── auth.py           # Token schemas
├── services/
│   ├── user_service.py   # User CRUD/auth logic
│   └── auth_service.py   # Token generation/refresh
├── api/
│   ├── deps.py           # Dependencies & role check
│   ├── routes_auth.py    # /auth endpoints
│   └── routes_users.py   # /users endpoints
└── tests/
  └── test_auth.py      # Basic auth test
```

## Implemented Endpoints

1. POST `/api/v1/auth/register` – create user, returns tokens
2. POST `/api/v1/auth/login` – username(email)/password, returns tokens
3. POST `/api/v1/auth/refresh` – refresh access token
4. GET `/api/v1/users/me` – current user profile
5. PUT `/api/v1/users/me` – update own email/password
6. GET `/api/v1/users/{user_id}` – admin/superadmin only

## Planned (Not Yet Implemented)

| Feature                            | Status  | Notes                           |
| ---------------------------------- | ------- | ------------------------------- |
| Password reset flow                | Pending | Add token/email sender service  |
| Email verification                 | Pending | Store verification tokens + TTL |
| Logout / token revoke endpoint     | Pending | Use blacklist + JTI             |
| Refresh token rotation enforcement | Partial | Need rotation + blacklist check |
| Role management endpoints          | Pending | Admin endpoints to assign roles |

## Production Hardening Suggestions

- Swap SQLite for Postgres (update `DATABASE_URL`)
- Use HTTPS & secure cookie tokens / OAuth2 flows
- Implement email verification & password reset
- Real rate limiting (Redis + slowapi)
- Structured logging / tracing (OpenTelemetry)
- CI pipeline (lint, tests, security scans, migrations)
- Refresh token rotation & revocation with JTI tracking
- Admin endpoints for role assignment & governance

## License

MIT
