Team Task Manager - README
==========================

A simple web app where admins can create projects, assign tasks to team members, 
and track progress. Built with Flask and MySQL.


HOW TO RUN LOCALLY
------------------

1. Make sure you have Python and MySQL installed.

2. Install required packages:
   pip install -r requirements.txt

3. Set up the database:
   mysql -u root -p < setup_db.sql

4. Run the app:
   python app.py

5. Open your browser and go to:
   http://localhost:5000


FEATURES
--------
- Signup and Login with role selection (Admin or Member)
- Admin can create Projects with a name and description
- Admin can create Tasks and assign them to members with a deadline
- Admin can see all tasks, delete tasks, and delete projects
- Member can see their own tasks sorted by deadline
- Member can mark tasks as Done
- Overdue tasks are highlighted in yellow on both dashboards
- Member dashboard shows a summary (total, pending, done, overdue)


ROLES
-----
- Admin: Can manage projects, create tasks, assign to members, delete tasks/projects
- Member: Can view their assigned tasks and mark them as done


PROJECT STRUCTURE
-----------------
app.py              - Main Flask application with all routes
setup_db.sql        - SQL file to create the database and tables
requirements.txt    - Python packages needed
Procfile            - For Railway deployment
templates/
    login.html          - Login and Signup page
    admin_dashboard.html - Admin panel
    member_dashboard.html - Member panel


DEPLOYMENT ON RAILWAY
---------------------

1. Push your code to a GitHub repository.

2. Go to https://railway.app and create a new project.

3. Click "Deploy from GitHub repo" and select your repository.

4. Add a MySQL database plugin in Railway.

5. In Railway, go to your app's Variables tab and add these:
   DB_HOST     = (from Railway MySQL plugin, the host value)
   DB_USER     = (from Railway MySQL plugin, the user value)
   DB_PASSWORD = (from Railway MySQL plugin, the password value)
   DB_NAME     = task_manager_db
   SECRET_KEY  = any_random_string_here

6. In the Railway MySQL shell, run the setup_db.sql file to create the tables:
   Copy the contents of setup_db.sql and paste it in the MySQL shell.

7. Railway will automatically detect the Procfile and deploy using gunicorn.

8. Your app will get a live URL like https://yourapp.up.railway.app


TECH STACK
----------
- Backend:  Python, Flask
- Database: MySQL
- Frontend: HTML, CSS (no frameworks, just plain HTML)
- Deploy:   Railway


NOTES
-----
- Passwords are stored as plain text (this is a beginner project, not production ready)
- No JavaScript frameworks used, just vanilla JS for the login/signup toggle
- All styles are written inline in the HTML files for simplicity
