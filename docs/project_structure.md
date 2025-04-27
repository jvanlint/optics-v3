# Project Structure

A clean project structure saves huge pain later when you add more apps and features.

I’ll give you a real-world, professional Django project structure that’s easy to maintain as your project grows — especially with multiple apps.

⸻

🏗️ Recommended Django Project Structure

Suppose your project is called myproject.

Here’s how your project root should look:

myproject/
│
├── manage.py
├── pyproject.toml            # (if you use modern packaging — recommended)
├── requirements.txt          # (or requirements/)
├── README.md
├── .env                      # (environment variables - SECRET_KEY, DB settings etc)
├── .gitignore
│
├── myproject/                # <-- main Django config package
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py           # base settings
│   │   ├── dev.py            # dev-specific settings
│   │   └── prod.py           # production-specific settings
│   ├── urls.py
│   └── wsgi.py
│
├── apps/                     # <-- where ALL your apps live
│   ├── core/                 # a "core" app, eg. homepage, dashboard
│   │   ├── migrations/
│   │   ├── templates/
│   │   │   └── core/
│   │   ├── static/
│   │   │   └── core/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests.py
│   │
│   ├── users/                # a users app (custom user model? auth?)
│   │   └── ...
│   │
│   └── another_app/          # more apps
│       └── ...
│
├── static/                   # collected static files (optional for local dev)
│
└── templates/                # global templates if needed

⸻

🧠 Key Best Practices Explained

Topic Best Practice Why
Multiple Apps Put ALL apps inside /apps/ Avoid cluttering root folder, scales cleanly
Settings Management Split settings into /settings/base.py, /settings/dev.py, /settings/prod.py Easier to manage different environments
Environment Variables Use .env + django-environ or python-decouple Never hard-code secrets or config in settings
Templates Each app manages its own templates inside templates/<app_name>/ Keeps templates modular and tied to app logic
Static Files Each app manages its own static inside static/<app_name>/ Same reason as templates; modular and neat
Tests Put small tests in each app, not one giant tests/ folder Makes tests easier to find and maintain
Naming Conventions App names should be short, lowercase, and plural (usually) E.g., users, orders, products — looks clean
Global Templates Use a /templates/ root folder only for global stuff (e.g., base.html) Keeps base layouts separate from app-specific stuff

⸻

🧩 Your settings/__init__.py

Set it up so Django knows which settings file to load:

# settings/__init__.py

import os

env = os.getenv('DJANGO_ENV', 'dev')

if env == 'prod':
    from .prod import *
else:
    from .dev import*

Then when you deploy, just set DJANGO_ENV=prod and it switches automatically.

⸻

🚀 Command to start a new app correctly

Instead of:

python manage.py startapp users

do:

python manage.py startapp users apps/users

This way it creates apps inside apps/, not littered in project root.

⸻

🛡 Bonus Best Practices
 • Use django-extensions for extra manage.py tools (like runserver_plus).
 • Use django-debug-toolbar in dev to monitor queries, templates, etc.
 • Set up black, ruff, isort for auto-formatting and linting.
 • Use pre-commit hooks early to enforce code style automatically.
 • Always plan for custom User models early (AbstractUser) even if you think you won’t need it now.

⸻

✨ Final Thought

Think of each app like a mini Django project:
models, views, templates, static, tests — self-contained — easy to maintain, migrate, or delete later if needed.

⸻

Would you like me to generate a full project skeleton (files + starter content) that you could literally just copy-paste and start from?
I can even set it up with Tailwind + HTMX pre-wired in if you want 🚀.
