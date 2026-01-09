# Project Management App

A simple **Project Management Web Application** built with **Flask**, **SQLite**, and **JWT authentication**.  
It allows **Admins** to create projects, add members, and manage tasks, while **Members** can view their assigned tasks and update their status.

---

## Features

- **Authentication**
  - User registration and login with email/password
  - Role-based access: Admin / Member
  - JWT-based authentication
- **Admin**
  - Create, update, delete projects
  - Add or remove members from projects
  - Create, edit, delete tasks
- **Member**
  - View assigned projects and tasks
  - Update task status
- **Frontend**
  - Responsive dashboard with project and task management
  - Login and registration pages
  - Task and project CRUD interfaces

---

## Project Structure

# Project Management App

A simple **Project Management Web Application** built with **Flask**, **SQLite**, and **JWT authentication**.  
It allows **Admins** to create projects, add members, and manage tasks, while **Members** can view their assigned tasks and update their status.

---

## Features

- **Authentication**
  - User registration and login with email/password
  - Role-based access: Admin / Member
  - JWT-based authentication
- **Admin**
  - Create, update, delete projects
  - Add or remove members from projects
  - Create, edit, delete tasks
- **Member**
  - View assigned projects and tasks
  - Update task status
- **Frontend**
  - Responsive dashboard with project and task management
  - Login and registration pages
  - Task and project CRUD interfaces

---

## Project Structure

Project_Management/
├── app.py # Main Flask app
├── extensions.py # DB and JWT initialization
├── models.py # Database models: User, Project, Task, ProjectMember
├── templates/ # HTML templates (dashboard, login, register)
├── static/ # CSS styles
├── instance/ # SQLite database files
├── test.http # Optional test HTTP requests
└── README.md # This file

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Ishika-tyagi/project-management-app-new.git
cd project-management-app-new

### 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

### 3.Install dependencies
pip install -r requirements.txt

### 4. Run the Flask app
python app.py
The app will run at: http://127.0.0.1:5000

Usage
Open the browser and go to /ui/register to create a new account.
Login at /ui/login.
Admin users can create projects, add members, and create tasks.
Members can view assigned projects and tasks in the dashboard.
Notes
Database: SQLite is used (instance/database.db)
Ignored files: __pycache__/, instance/ folder, and environment files are ignored via .gitignore.
Optional Testing
You can test API endpoints using the provided test.http file in VS Code with the REST Client extension.
Author
Ishika Tyagi
Full-Stack Developer | Project Management App

