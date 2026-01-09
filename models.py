from extensions import db

# ----------------- USER -----------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="Member")  # Admin / Member

    projects = db.relationship("Project", backref="owner", lazy=True)
    tasks = db.relationship("Task", backref="assignee", lazy=True)
    memberships = db.relationship("ProjectMember", backref="user", lazy=True)


# ----------------- PROJECT -----------------
class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    members = db.relationship("ProjectMember", backref="project", lazy=True)
    tasks = db.relationship("Task", backref="project", lazy=True)


# ----------------- PROJECT MEMBER -----------------
class ProjectMember(db.Model):
    __tablename__ = "project_members"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


# ----------------- TASK -----------------
class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(db.String(20), default="Todo")  # Todo / In Progress / Done
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey("users.id"))
