# Project Management App

A Flask-based project management application with user authentication, projects, tasks, and member management.

## Features

- User registration and login (Admin / Member)
- JWT-based authentication
- Admin can create projects, add/remove members
- Admin can create tasks and assign them to members
- Members can view their assigned tasks
- Dashboard UI with CRUD functionality for projects and tasks

## Tech Stack

- Backend: Flask, Flask-SQLAlchemy, Flask-JWT-Extended
- Database: SQLite
- Frontend: HTML, CSS, JavaScript

## Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/Ishika-tyagi/project-management-app.git
cd project-management-app
Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies
pip install -r requirements.txt
Run the application
python app.py
Open in browser
Go to http://127.0.0.1:5000/ui/login

---

### **4️⃣ Stage and commit README + requirements**

```bash
git add README.md requirements.txt
git commit -m "Add README with setup instructions and requirements"
