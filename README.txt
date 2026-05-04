Team Task Manager - README

A simple web application where admins can create projects, assign tasks to team members, and track their progress. Built using Flask and PostgreSQL, and deployed on Render.

HOW TO RUN LOCALLY

1. Make sure you have Python installed.
2. Install required packages:
    pip install -r requirements.txt
3. Set up the PostgreSQL database and update your DATABASE_URL in environment variables.
4. Run the app:
    python app.py
5. Open your browser and go to:
    http://localhost:5000

FEATURES

* Signup and Login with role selection (Admin or Member)
* Admin can create Projects with name and description
* Admin can create Tasks, assign them to members with deadlines
* Admin can view all tasks and projects
* Member can view their assigned tasks sorted by deadline
* Member can mark tasks as Done and update progress
* Overdue tasks are highlighted
* Member dashboard shows task summary (total, pending, done, overdue)

ROLES

* Admin: Can manage projects, create tasks, assign to members
* Member: Can view assigned tasks and update status/progress

PROJECT STRUCTURE

app.py              - Main Flask application with routes
requirements.txt    - Required Python packages
templates/
login.html              - Login and Signup page
admin_dashboard.html    - Admin dashboard
member_dashboard.html  - Member dashboard

DEPLOYMENT ON RENDER

1. Push your project to a GitHub repository.
2. Go to https://render.com and create a new Web Service.
3. Connect your GitHub repository and select the project.
4. Render will auto-detect Python and Flask setup.
5. Set the following:
    Build Command:
    pip install -r requirements.txt
    Start Command:
    gunicorn app:app
6. Add Environment Variables:
    DATABASE_URL = (from Render PostgreSQL dashboard)
    SECRET_KEY  = any_random_string
7. Create a PostgreSQL database in Render.
8. Copy the External Database URL and paste it into DATABASE_URL.
9. Open database shell (psql) and run the SQL file to create tables.
10. Deploy the service. Render will provide a live URL.

TECH STACK

* Backend: Python, Flask
* Database: PostgreSQL
* Frontend: HTML, CSS
* Deployment: Render

NOTES

* Passwords are stored as plain text (for learning purpose)
* Simple UI without any frontend framework
* Designed as a beginner-friendly full stack project
