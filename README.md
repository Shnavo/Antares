# Antares

## Example structure:

# Project Directory Structure

```text
📁 antares_project/
│
├── 📄 .env                    # Secret environment credentials (git ignored)
├── 📄 .gitignore              # Tells Git to ignore venv/, .env, and local database data
├── 📄 docker-compose.yml      # Orchestrates your local Postgres & pgAdmin containers
├── 📄 requirements.txt        # Backend Python dependencies (FastAPI, SQLAlchemy, etc.)
├── 📄 README.md               #
|
├── 📁 backend/                # Everything Python/FastAPI lives here
│   ├── 📄 main.py             # Entry point (initializes FastAPI app and includes routers)
│   │
│   └── 📁 app/
│       ├── 📄 __init__.py
│       ├── 📄 config.py       # Reads and validates settings from your .env file
│       ├── 📄 database.py     # Sets up SQLAlchemy engine, sessions, and get_db() dependency
│       ├── 📄 auth.py         # Security utilities (hashing passwords, JWT generation)
│       │
│       ├── 📁 models/         # Database Architecture (SQLAlchemy Models)
│       │   ├── 📄 __init__.py
│       │   └── 📄 user.py     # Class User(Base): __tablename__ = "users"
│       │
│       ├── 📁 schemas/        # Request/Response Data Validation (Pydantic Models)
│       │   ├── 📄 __init__.py
│       │   └── 📄 user.py     # class UserCreate(BaseModel), class UserOut(BaseModel)
│       │
│       └── 📁 routers/        # API Controller endpoints (keeps main.py completely clean)
│           ├── 📄 __init__.py
│           ├── 📄 auth.py     # Handles /register and /login endpoints
│           └── 📄 todos.py    # Handles CRUD actions for your todo dashboards
│
└── 📁 frontend/               # The browser presentation layer
    ├── 📁 static/             # Assets served directly to the client browser
    │   ├── 📁 css/
    │   │   └── 📄 styles.css  # Global application layouts
    │   └── 📁 js/
    │       └── 📄 app.js      # Handles browser-side fetch() API calls to the backend
    │
    └── 📁 templates/          # HTML structures
        ├── 📄 login.html      # Authentication screen
        └── 📄 index.html      # Main user dashboard interface
```

#### TO-DO
[ ] change .env to secrets before deployment

# Dependencies
requirements.txt exists but actually only 3 pip installs are required:
- pip install psycopg2-binary
- pip install python-dotenv
- pip install "fastapi[standard]"
