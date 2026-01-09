# app.py
from flask import Flask, render_template, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from extensions import db, jwt
from models import User, Project, ProjectMember, Task

app = Flask(__name__)

# ---------------- CONFIG ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret-key"

db.init_app(app)
jwt.init_app(app)

# ---------------- FRONTEND PAGES ----------------
@app.route("/ui/login")
def ui_login():
    return render_template("login.html")

@app.route("/ui/register")
def ui_register():
    return render_template("register.html")

@app.route("/ui/dashboard")
def ui_dashboard():
    return render_template("dashboard.html")

# ---------------- HOME ----------------
@app.route("/")
def home():
    return {"message": "Project Management API running"}

# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "Member")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(
        email=email,
        password=generate_password_hash(password),
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()

    if not user or not check_password_hash(user.password, data.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role, "email": user.email}
    )

    return jsonify({"access_token": token})

# ---------------- USERS CRUD ----------------
@app.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    role = get_jwt()["role"]
    if role != "Admin":
        return jsonify({"error": "Only Admin can view users"}), 403
    users = User.query.all()
    return jsonify([{"id": u.id, "email": u.email, "role": u.role} for u in users])

# ---------------- PROJECTS CRUD ----------------
@app.route("/projects", methods=["POST"])
@jwt_required()
def create_project():
    user_id = int(get_jwt_identity())
    role = get_jwt()["role"]
    if role != "Admin":
        return jsonify({"error": "Only Admin can create projects"}), 403

    name = request.get_json().get("name")
    if not name:
        return jsonify({"error": "Project name required"}), 400

    project = Project(name=name, owner_id=user_id)
    db.session.add(project)
    db.session.commit()

    return jsonify({"message": "Project created successfully", "project_id": project.id}), 201

@app.route("/projects", methods=["GET"])
@jwt_required()
def get_projects():
    user_id = int(get_jwt_identity())
    owned = Project.query.filter_by(owner_id=user_id).all()
    memberships = ProjectMember.query.filter_by(user_id=user_id).all()
    result = []
    for p in owned:
        result.append({"id": p.id, "name": p.name, "role": "Owner"})
    for m in memberships:
        project = Project.query.get(m.project_id)
        if project:
            result.append({"id": project.id, "name": project.name, "role": "Member"})
    return jsonify(result)

@app.route("/projects/<int:project_id>", methods=["PUT"])
@jwt_required()
def update_project(project_id):
    user_id = int(get_jwt_identity())
    project = Project.query.get_or_404(project_id)
    if project.owner_id != user_id:
        return jsonify({"error": "Only owner can update project"}), 403
    data = request.get_json()
    project.name = data.get("name", project.name)
    db.session.commit()
    return jsonify({"message": "Project updated"})

@app.route("/projects/<int:project_id>", methods=["DELETE"])
@jwt_required()
def delete_project(project_id):
    user_id = int(get_jwt_identity())
    project = Project.query.get_or_404(project_id)
    if project.owner_id != user_id:
        return jsonify({"error": "Only owner can delete project"}), 403
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted"})

# ---------------- PROJECT MEMBERS ----------------
@app.route("/projects/<int:project_id>/add-member", methods=["POST"])
@jwt_required()
def add_member(project_id):
    user_id = int(get_jwt_identity())
    project = Project.query.get_or_404(project_id)
    if project.owner_id != user_id:
        return jsonify({"error": "Only owner can add members"}), 403

    member_email = request.get_json().get("email")
    if not member_email:
        return jsonify({"error": "Email is required"}), 400

    member_user = User.query.filter_by(email=member_email).first()
    if not member_user:
        return jsonify({"error": "User not found"}), 404

    member_id = member_user.id

    if ProjectMember.query.filter_by(project_id=project_id, user_id=member_id).first():
        return jsonify({"error": "User already added"}), 400

    db.session.add(ProjectMember(project_id=project_id, user_id=member_id))
    db.session.commit()
    return jsonify({"message": f"{member_email} added successfully"})


@app.route("/projects/<int:project_id>/remove-member-by-email", methods=["DELETE"])
@jwt_required()
def remove_member_by_email(project_id):
    user_id = int(get_jwt_identity())
    project = Project.query.get_or_404(project_id)
    
    if project.owner_id != user_id:
        return jsonify({"error": "Only owner can remove members"}), 403

    member_email = request.get_json().get("email")
    if not member_email:
        return jsonify({"error": "Email required"}), 400

    member_user = User.query.filter_by(email=member_email).first()
    if not member_user:
        return jsonify({"error": "User not found"}), 404

    member = ProjectMember.query.filter_by(project_id=project_id, user_id=member_user.id).first()
    if not member:
        return jsonify({"error": "Member not in project"}), 404

    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": f"{member_email} removed successfully"})

# ---------------- TASKS CRUD ----------------
@app.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())
    role = get_jwt()["role"]
    data = request.get_json()
    project = Project.query.get_or_404(data["project_id"])

    if role != "Admin" and project.owner_id != user_id:
        return jsonify({"error": "Not allowed"}), 403

    assigned_email = data.get("assigned_email")
    assigned_to = None
    if assigned_email:
        user = User.query.filter_by(email=assigned_email).first()
        if user:
            assigned_to = user.id

    task = Task(
        title=data["title"],
        description=data.get("description"),
        project_id=data["project_id"],
        assigned_to=assigned_to
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created", "task_id": task.id}), 201


@app.route("/projects/<int:project_id>/tasks", methods=["GET"])
@jwt_required()
def get_tasks(project_id):
    user_id = int(get_jwt_identity())
    role = get_jwt()["role"]
    project = Project.query.get_or_404(project_id)
    tasks = Task.query.filter_by(project_id=project_id)
    if role != "Admin":
        tasks = tasks.filter((Task.assigned_to==user_id) | (Task.assigned_to==None))
    tasks = tasks.all()
    result = []
    for t in tasks:
        assigned_email = User.query.get(t.assigned_to).email if t.assigned_to else None
        result.append({
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "assigned_to": t.assigned_to,
            "assigned_to_email": assigned_email,
            "status": t.status
        })
    return jsonify(result)


@app.route("/my-tasks", methods=["GET"])
@jwt_required()
def my_tasks():
    user_id = int(get_jwt_identity())
    role = get_jwt()["role"]
    if role == "Admin":
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(assigned_to=user_id).all()
    result = []
    for t in tasks:
        assigned_email = User.query.get(t.assigned_to).email if t.assigned_to else None
        result.append({
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "project_id": t.project_id,
            "status": t.status,
            "assigned_to_email": assigned_email
        })
    return jsonify(result)


@app.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    user_id = int(get_jwt_identity())
    role = get_jwt()["role"]
    task = Task.query.get_or_404(task_id)
    if role != "Admin" and task.assigned_to != user_id:
        return jsonify({"error": "Not allowed"}), 403
    data = request.get_json()

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)

    assigned_email = data.get("assigned_email")
    if assigned_email:
        user = User.query.filter_by(email=assigned_email).first()
        if user:
            task.assigned_to = user.id

    db.session.commit()
    return jsonify({"message": "Task updated"})


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())
    role = get_jwt()["role"]
    task = Task.query.get_or_404(task_id)
    if role != "Admin" and task.assigned_to != user_id:
        return jsonify({"error": "Not allowed"}), 403
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})

# ---------------- RUN ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
