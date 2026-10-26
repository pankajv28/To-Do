# To-Do App

A personal task-management web app built to help me develop discipline through consistent planning, execution, and review. The project is both a practical tool for organizing my work and a way to learn web development by building and improving a real application.

## Inspiration

I built this app to make discipline easier to practise. Instead of keeping tasks scattered across notes or relying on memory, I wanted one place where I could decide what to do, see what I am working on, and track what I have completed.

The project is also a hands-on learning exercise: building a useful application from the database layer through the web interface, then running it locally and deploying it.

## What the app currently does

### Task management
- Organizes tasks into three status columns:
  - **Planned** (`tostart`)
  - **Ongoing** (`ongoing`)
  - **Done** (`done`)
- Creates tasks with a title, optional description, status, and creation date.
- Limits task titles to 50 characters.
- Opens a task-details dialog showing its description, status, and creation date.
- Allows tasks to be edited, moved between statuses, and deleted.
- Stores tasks in SQLite so they persist between sessions.
- Keeps each task associated with a user account.

### Accounts and user administration
- Provides a login page.
- Stores password hashes rather than plain-text passwords.
- Uses Flask sessions to keep users logged in.
- Filters task queries by the logged-in user's ID.
- Provides an administrator page to view users by group, create users, change passwords, and delete users.
- Prevents the currently logged-in user from deleting their own account through the admin page.
- Displays success and error feedback using Flask flash messages.

## Technology

- **Python** — application logic.
- **Flask** — web framework and routes.
- **SQLite** — persistent database.
- **HTML** — page structure and forms.
- **CSS** — task board, dialogs, and page styling.
- **JavaScript** — dialog interactions and client-side user filtering.
- **Werkzeug** — password hashing and verification, plus proxy middleware support.
- **Gunicorn** — production WSGI server option.
- **Nginx + systemd** — deployment components used for serving and managing the app on a Linux server.

## Project structure

```text
todo/
├── app.py                 # Flask routes and application setup
├── init_db.py             # Creates database tables
├── todo.py                # Task database operations
├── manage_users.py        # User creation, login, password and admin operations
├── requirements.txt       # Python dependencies
├── todo.db                # Local SQLite database (do not commit real user data)
├── templates/
│   ├── index.html         # Task board and task dialogs
│   ├── login.html         # Login page
│   └── admin.html         # User administration page
└── static/
    ├── styles.css         # Shared styling
    └── admin_page.css     # Admin-page styling
```

## Run locally

### 1. Get the project and enter its directory

```bash
cd todo
```

If you use Git, clone the repository first and then enter the project directory.

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Initialize the database

```bash
python init_db.py
```

Run this from the project directory, because the database code currently opens `todo.db` using a relative path.

### 5. Configure the Flask secret

Set a strong secret key in your environment rather than keeping it hard-coded in `app.py`.

**Windows PowerShell:**

```powershell
$env:FLASK_SECRET_KEY = "replace-with-a-long-random-secret"
```

**macOS / Linux:**

```bash
export FLASK_SECRET_KEY="replace-with-a-long-random-secret"
```

Then configure `app.py` to read `FLASK_SECRET_KEY` from the environment. Use the same secret consistently for the running deployment, and never commit real secrets to version control.

### 6. Start the development server

The project includes a development entry point in `app.py` that runs on port `5001`:

```bash
python app.py
```

Open <http://127.0.0.1:5001/> in your browser.

For local development, you can also use Flask's CLI:

```bash
flask --app app run --port 5001 --debug
```

Use the Flask development server for local development only, not as the production server.

### 7. Run with Gunicorn (Linux/macOS or a compatible environment)

Install Gunicorn if it is not already installed:

```bash
python -m pip install gunicorn
```

Then run:

```bash
gunicorn --bind 127.0.0.1:8000 app:app
```

This starts Gunicorn on port `8000`. A production deployment can put Nginx in front of Gunicorn and manage the process with systemd. Configure the service, environment variables, paths, and Nginx routing for your own server.

## Database and data safety

- `init_db.py` creates tables if they do not already exist; it is not a complete database-migration tool.
- Back up `todo.db` before making schema changes.
- Add local databases, virtual environments, Python cache files, and secrets to `.gitignore`.
- Database operations currently use a relative path (`todo.db`), so run commands from the project directory or update the code to use an explicit database path.

## Planned improvements

These are ideas for future iterations, not features that are already implemented.

### Task-board improvements
- [ ] Add projects so tasks can be grouped under a larger goal or project.
- [ ] Add an archive option for tasks in the **Done** column, keeping the active board uncluttered.
- [ ] Show the number of tasks in each column heading.
- [ ] Show how many days ago each task was created in the **Planned** and **Ongoing** columns.
- [ ] Add sorting and filtering, such as by creation date, project, or status.
- [ ] Add task priorities and due dates.
- [ ] Add search across task titles and descriptions.
- [ ] Improve validation and show friendly messages for invalid task input.
- [ ] Add confirmation and feedback patterns consistently for task actions.

### Discipline and review
- [ ] Add a daily or weekly review of completed tasks.
- [ ] Show completion statistics over time.
- [ ] Track overdue or long-running tasks.
- [ ] Add a lightweight dashboard for progress by project and status.

### Engineering and reliability
- [ ] Move the Flask secret key into an environment variable and rotate any key that has been exposed.
- [ ] Add role-based authorization checks to every user-administration route.
- [ ] Add database migrations for future schema changes.
- [ ] Add automated tests for task operations, authentication, and permissions.
- [ ] Add CSRF protection to state-changing forms.
- [ ] Improve production logging and error pages.
- [ ] Add static-asset cache versioning so updated CSS and JavaScript are picked up reliably after deployment.
- [ ] Document deployment and backup/restore procedures.

## Current limitations

- The app currently uses SQLite.
- The current task model has a title, description, status, creation date, and user association; projects, archiving, due dates, and priorities are not implemented yet.
- Review access controls and production security settings before exposing the app publicly.