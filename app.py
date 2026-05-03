from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os
from datetime import date

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "mysecretkey123")


# ------- DB CONNECTION -------
def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "8888990599"),
        database=os.environ.get("DB_NAME", "task_manager_db")
    )


# ------- HOME / LOGIN PAGE -------
@app.route("/")
def index():
    return render_template("login.html")


# ------- LOGIN -------
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s AND role=%s",
        (username, password, role)
    )

    user = cursor.fetchone()
    db.close()

    if user:
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]

        return redirect("/admin" if role == "admin" else "/member")

    return render_template("login.html", error="Invalid credentials")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    db = get_db()
    cursor = db.cursor()
@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # check if user exists
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    existing = cursor.fetchone()

    if existing:
        db.close()
        return render_template("login.html", error="User already exists")

    # insert new user
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
        (username, password, role)
    )

    db.commit()
    db.close()

    return render_template("login.html", signup_success=True)
    # check if user already exists
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    existing = cursor.fetchone()

    if existing:
        db.close()
        return "User already exists"

    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
        (username, password, role)
    )

    db.commit()
    db.close()

    return redirect("/")
# ------- ADMIN DASHBOARD -------
@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect("/")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # PROJECTS
    cursor.execute("SELECT * FROM projects ORDER BY id DESC")
    projects = cursor.fetchall()

    # TASKS (✅ added progress)
    cursor.execute("""
        SELECT tasks.id, tasks.title, tasks.deadline, tasks.status,
               tasks.progress,
               users.username as assigned_to,
               projects.name as project_name
        FROM tasks
        JOIN users ON tasks.assigned_to = users.id
        JOIN projects ON tasks.project_id = projects.id
        ORDER BY tasks.deadline ASC
    """)
    tasks = cursor.fetchall()
    db.close()

    today = date.today()
    for task in tasks:
        task["overdue"] = (
            task["status"] == "pending"
            and task["deadline"] is not None
            and task["deadline"] < today
        )

    return render_template("admin_dashboard.html",
                           username=session["username"],
                           projects=projects,
                           tasks=tasks)


# ------- CREATE PROJECT PAGE -------
@app.route("/create_project_page")
def create_project_page():
    if session.get("role") != "admin":
        return redirect("/")
    return render_template("create_project.html")


# ------- CREATE TASK PAGE -------
@app.route("/create_task_page")
def create_task_page():
    if session.get("role") != "admin":
        return redirect("/")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id, username FROM users WHERE role='member'")
    members = cursor.fetchall()

    cursor.execute("SELECT id, name FROM projects")
    projects = cursor.fetchall()

    db.close()

    return render_template("create_task.html",
                           members=members,
                           projects=projects)


# ------- CREATE PROJECT -------
@app.route("/create_project", methods=["POST"])
def create_project():
    if session.get("role") != "admin":
        return redirect("/")

    name = request.form["name"]
    description = request.form["description"]

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO projects (name, description, created_by) VALUES (%s, %s, %s)",
        (name, description, session["user_id"])
    )

    db.commit()
    db.close()

    return redirect("/admin")


# ------- CREATE TASK -------
@app.route("/create_task", methods=["POST"])
def create_task():
    if session.get("role") != "admin":
        return redirect("/")

    title = request.form["title"]
    member_id = request.form["member_id"]
    deadline = request.form["deadline"]
    project_id = request.form["project_id"]

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, assigned_to, deadline, status, project_id, progress, notified) VALUES (%s, %s, %s, 'pending', %s, 0, 0)",
        (title, member_id, deadline, project_id)
    )

    db.commit()
    db.close()

    return redirect("/admin")


# ------- MANAGE MEMBERS -------
@app.route('/manage_members')
def manage_members():
    if session.get("role") != "admin":
        return redirect("/")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT users.username,
               tasks.title AS task_title,
               projects.name AS project_name,
               tasks.status
        FROM tasks
        JOIN users ON tasks.assigned_to = users.id
        JOIN projects ON tasks.project_id = projects.id
        ORDER BY users.username
    """

    cursor.execute(query)
    data = cursor.fetchall()
    db.close()

    return render_template("manage_members.html", member_tasks=data)


# ------- MEMBER DASHBOARD -------
@app.route("/member")
def member_dashboard():
    if session.get("role") != "member":
        return redirect("/")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # TASKS (unchanged + safe)
    cursor.execute("""
        SELECT tasks.id, tasks.title, tasks.deadline, tasks.status,
               tasks.progress,
               projects.name as project_name
        FROM tasks
        JOIN projects ON tasks.project_id = projects.id
        WHERE tasks.assigned_to=%s
        ORDER BY tasks.deadline ASC
    """, (session["user_id"],))

    tasks = cursor.fetchall()

    # 🔥 NEW: GET TASKS WITH ADMIN NAME
    cursor.execute("""
        SELECT tasks.title,
               projects.name as project_name,
               tasks.deadline,
               admin.username as admin_name
        FROM tasks
        JOIN projects ON tasks.project_id = projects.id
        JOIN users as admin ON projects.created_by = admin.id
        WHERE tasks.assigned_to=%s AND tasks.notified=0
    """, (session["user_id"],))

    new_tasks = cursor.fetchall()

    # UPDATE notified flag
    cursor.execute("""
        UPDATE tasks SET notified=1
        WHERE assigned_to=%s AND notified=0
    """, (session["user_id"],))

    db.commit()
    db.close()

    # OVERDUE CHECK (same logic)
    today = date.today()
    for task in tasks:
        task["overdue"] = (
            task["status"] == "pending"
            and task["deadline"] is not None
            and task["deadline"] < today
        )

    return render_template("member_dashboard.html",
                           username=session["username"],
                           tasks=tasks,
                           new_tasks=new_tasks)


# ------- MARK DONE -------
@app.route("/mark_done/<int:task_id>", methods=["POST"])
def mark_done(task_id):
    if session.get("role") != "member":
        return redirect("/")

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE tasks SET status='done' WHERE id=%s AND assigned_to=%s",
        (task_id, session["user_id"])
    )

    db.commit()
    db.close()

    return redirect("/member")


# ------- UPDATE PROGRESS -------
@app.route("/update_progress/<int:task_id>/<int:value>", methods=["POST"])
def update_progress(task_id, value):
    if session.get("role") != "member":
        return redirect("/")

    db = get_db()
    cursor = db.cursor()

    # 🔥 If progress = 100 → mark as done
    if value == 100:
        cursor.execute(
            "UPDATE tasks SET progress=%s, status='done' WHERE id=%s AND assigned_to=%s",
            (value, task_id, session["user_id"])
        )
    else:
        cursor.execute(
            "UPDATE tasks SET progress=%s WHERE id=%s AND assigned_to=%s",
            (value, task_id, session["user_id"])
        )

    db.commit()
    db.close()

    return redirect("/member")  

# ------- LOGOUT -------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ------- RUN APP -------
if __name__ == "__main__":
    app.run(debug=True)