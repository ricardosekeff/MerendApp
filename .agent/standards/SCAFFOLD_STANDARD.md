# FLASK & DOCKER STANDARD SCAFFOLD

**CRITICAL DIRECTIVE:** All generated projects MUST follow this exact directory and file structure. Do not deviate, invent, or suppress any of the paths defined below. This is a hard constraint.

project_root/
├── app/                        # Main Application Package
│   ├── __init__.py             # Flask App Factory (create_app function setup)
│   ├── extensions.py           # Instantiation of Flask extensions (SQLAlchemy, Migrate)
│   ├── models/                 # SQLAlchemy ORM Models (Shared domain logic)
│   │   ├── __init__.py
│   │   └── base.py             # Abstract base classes and mixins
│   ├── api/                    # [BLUEPRINT] API Service (Machine-to-Machine / REST)
│   │   ├── __init__.py         # API Blueprint registration
│   │   ├── routes.py           # RESTful endpoints returning JSON
│   │   ├── schemas.py          # Marshmallow serializers for input/output validation
│   │   └── errors.py           # Standardized JSON error handlers (404, 400, 500)
│   ├── web/                    # [BLUEPRINT] Frontend Service (Human-to-Machine)
│   │   ├── __init__.py         # Web Blueprint registration
│   │   ├── routes.py           # View functions utilizing render_template
│   │   └── forms.py            # Flask-WTF Forms for CSRF protection and validation
│   ├── static/                 # Static Assets
│   │   ├── css/                # Custom CSS (must not override Bootstrap core unnecessarily)
│   │   ├── js/                 # Client-side JavaScript
│   │   └── img/                # Image assets
│   └── templates/              # Jinja2 Templates (Strictly Bootstrap 5 compliant)
│       ├── base.html           # Master layout with navigation and CDN links
│       └── components/         # Reusable HTML fragments (e.g., _navbar.html, _footer.html)
├── tests/                      # Pytest suite directory
│   ├── conftest.py             # Test fixtures and test database setup
│   └── test_routes.py          # E2E and unit tests covering both blueprints
├── config.py                   # Configuration objects (Config, DevelopmentConfig, ProductionConfig)
├── run.py                      # Application entry point (imports create_app)
├── Dockerfile                  # Production-ready, multi-stage Dockerfile for Python/Flask
├── docker-compose.yml          # Container orchestration (Web service + PostgreSQL service)
├── requirements.txt            # Python dependencies (Flask, psycopg2-binary, gunicorn, etc.)
└── .env.example                # Template for environment variables (DB credentials, secret keys)