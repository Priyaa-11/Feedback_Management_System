# Feedback Management System

A Django-based web application for managing student feedback in educational institutions. The system allows students to log in and submit feedback for their teachers, and enables administrators (Principals) to manage students, teachers, and view feedback submissions.

## Features

### Admin (Principal) Features
- Secure login / logout
- Dashboard with statistics (Total Students, Total Teachers, Total Feedback)
- Manage students (Add, View, Delete)
- Manage teachers (Add, View, Delete)
- View all feedback submissions
- View student name, roll number, teacher name, rating, description, and submission date
- Delete confirmation for safety

### Student Features
- Secure login / logout
- Student dashboard showing profile information
- Auto-filled profile details (Name, Roll Number, Department) — cannot be edited
- Select teacher from dropdown (only teachers not yet rated)
- Interactive 5-star rating system
- Write feedback description
- Submit feedback for multiple teachers
- Cannot submit duplicate feedback for the same teacher
- Thank You confirmation page after submission

## Technology Stack

- **Backend:** Python, Django 6.1
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (no frameworks)
- **Database:** SQLite (development), PostgreSQL (production)
- **ORM:** Django ORM
- **Authentication:** Django built-in authentication system
- **Deployment:** Railway / Render / PythonAnywhere

## Prerequisites

Before running this project, ensure you have:

- **Python 3.10+** installed (Download from: https://www.python.org/downloads/)
- **Git** (optional, for version control) (Download from: https://git-scm.com/downloads)

## Installation and Setup

### Step 1: Clone the Project

```bash
git clone <your-repository-url>
cd Feedback_Management_System
```

### Step 2: Create Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Copy the environment file:

```bash
cp .env.example .env
```

Edit `.env` file and update the values:

```text
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Principal Account)

```bash
python manage.py createsuperuser
```

Enter:
- **Username:** admin (or your choice)
- **Email:** admin@college.edu
- **Password:** (a strong password)

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

### Step 8: Access the Application

Open your browser and visit: http://127.0.0.1:8000/

## Usage Guide

### Admin Login
1. Go to the login page.
2. Enter the superuser credentials you created.
3. You will be redirected to the Admin Dashboard.

### Adding Teachers
1. Login as admin.
2. Click "Teachers" in the navigation bar.
3. Click "+ Add Teacher".
4. Enter teacher name, department, and email.
5. Click Submit.

### Adding Students
1. Login as admin.
2. Click "Students" in the navigation bar.
3. Click "+ Add Student".
4. Fill in the student details (username, password, roll number, name, department, email, phone, address).
5. Click Submit. The system automatically creates both the Django User and the Student profile.

### Student Login
1. Go to the login page.
2. Enter the username and password you set when adding the student.
3. You will be redirected to the Student Dashboard.

### Submitting Feedback
1. Login as a student.
2. Click "+ Submit New Feedback".
3. Verify the auto-filled details (Roll Number, Name, Department).
4. Select a teacher from the dropdown.
5. Click stars for rating (1-5).
6. Write your feedback in the description box.
7. Click Submit Feedback.
8. You will see the Thank You page.

### Viewing Feedback (Admin)
1. Login as admin.
2. Click "Feedback" in the navigation bar.
3. View all feedback submissions with student name, roll number, teacher name, rating, description, and date.

## Project Structure

```text
feedback_management_system/
│
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── feedback_system/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/
│   ├── models.py       (Student model)
│   ├── views.py        (Login redirect logic)
│   ├── urls.py
│   └── admin.py
│
├── feedback_app/
│   ├── models.py       (Teacher, Feedback models)
│   ├── views.py        (Admin & Student views)
│   ├── urls.py
│   └── admin.py
│
├── templates/
│   ├── base.html
│   ├── 404.html
│   ├── registration/
│   │   └── login.html
│   ├── admin_panel/
│   │   ├── dashboard.html
│   │   ├── manage_students.html
│   │   ├── add_student.html
│   │   ├── manage_teachers.html
│   │   ├── add_teacher.html
│   │   └── view_feedback.html
│   └── student/
│       ├── dashboard.html
│       ├── feedback_form.html
│       └── thank_you.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── star_rating.js
```

## Database Schema

### User (Django Built-in)
- username (unique)
- password (hashed)
- email
- is_staff (for admin)
- is_superuser (for principal)

### Student
- user (OneToOne to User)
- name
- roll_number (unique)
- department
- email
- phone
- address

### Teacher
- name
- department
- email

### Feedback
- student (ForeignKey to Student)
- teacher (ForeignKey to Teacher)
- rating (1-5)
- description
- created_at

## Role-Based Access

### Admin (Principal)
- **Can access:** Dashboard, Students, Teachers, Feedback
- **Can perform:** Add/Delete students and teachers, View all feedback
- **Cannot:** Submit feedback (blocked by `user_passes_test` decorator)

### Student
- **Can access:** Student Dashboard, Feedback Form, Thank You page
- **Can perform:** Submit feedback, view own feedback history
- **Cannot:** Access admin pages (blocked by `user_passes_test` decorator)

## Security Features

- CSRF protection on all forms
- Password hashing using Django's built-in system
- Session-based authentication
- Role-based access control (decorators: `is_admin`, `is_student`)
- Server-side validation (rating 1-5, no empty descriptions)
- Duplicate feedback prevention (per student per teacher)
- SQL injection protection (Django ORM)
- XSS protection (Django templates)

## Deployment

### Recommended: Railway
1. Push your code to GitHub.
2. Sign up at https://railway.app/ using GitHub.
3. Create a new project from your GitHub repo.
4. Add a PostgreSQL database.
5. Set environment variables: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `DATABASE_URL`.
6. Deploy.

### Alternative: Render or PythonAnywhere
Both platforms support Django with the same environment variables.

## Troubleshooting

### CSRF Token Error
**Solution:** Refresh the page or clear browser cookies, then log in again.

### Student Login Fails
**Solution:** Make sure the student was created via the FMS Admin Panel (not the Django Admin), which properly creates both User and Student profile.

### Session Data Corrupted
**Solution:** Log out, close the browser tab, and log back in.

### Static Files Not Loading
**Solution:** Run `python manage.py collectstatic` to gather static files.

## Testing Checklist

### Admin Tests
- [ ] Login with admin credentials
- [ ] View dashboard statistics
- [ ] Add new student
- [ ] Delete student
- [ ] Add new teacher
- [ ] Delete teacher
- [ ] View all feedback

### Student Tests
- [ ] Login with student credentials
- [ ] View auto-filled profile
- [ ] Select teacher from dropdown
- [ ] Click star rating
- [ ] Write feedback description
- [ ] Submit feedback
- [ ] See Thank You page
- [ ] Verify duplicate prevention

### Security Tests
- [ ] Student cannot access `/admin-dashboard/`
- [ ] Admin cannot access `/student-dashboard/`
- [ ] Unauthenticated users redirected to login
- [ ] CSRF tokens present in all forms
