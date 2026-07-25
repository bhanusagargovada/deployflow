# Project Management & Deployment Tracking System

A professional Flask application for managing projects, tasks, releases, users and reports.

Quick start

1. Create a virtualenv and install dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and update values.
3. Initialize the database and run migrations.
4. Run the app:

```bash
python run.py
```

Additional notes: this project no longer includes Docker artifacts. Run the app locally using the Python instructions above.

Additional features implemented:

- Authentication (register, login, logout, forgot/reset password)
- Role-based access control (Administrator, Project Manager, Team Member)
- Projects: create, edit, delete, search, filter, pagination
- Tasks: create, assign, status, progress, comments, pagination
- Releases: record releases, release history, PDF export
- Reports: project/task/release PDF reports via ReportLab
- Dashboard with Chart.js visualizations (project status, monthly projects, task completion, user productivity)
- Notifications (in-app + email fallback) and activity logs
- Admin panel for user management and activity viewing
- Profile and Settings pages

Running tests

Install `pytest` then run:

```bash
pip install pytest
pytest -q
```

Notes
- Update `.env` with `DATABASE_URI` (MySQL) and `SECRET_KEY`.
- If `MAIL_SERVER` is not set, emails (password reset, notifications) are printed to the console for development.
- Database migrations are handled with Flask-Migrate. Use the `flask` CLI as described below.

Local development commands (Windows PowerShell):

```powershell
set FLASK_APP=run.py
set FLASK_ENV=development
flask db init       # only first time
flask db migrate -m "initial"
flask db upgrade
python run.py
```

If you want me to continue, I can:

- Add inline reply forms and pagination for comment threads.
- Add notification center improvements (mark all read, filters).
- Expand test coverage with integration tests using Flask test client.
- Add more report templates and export options.

