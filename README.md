

ECHO is on.
Django Project

Overview

This project is a user authentication system with two types of users: Teacher and Student. It uses Django Rest Framework (DRF) for the backend, JWT authentication, and a PostgreSQL database with environment variable setup. The frontend is built using HTML, CSS, and JavaScript.

Features

User Registration: Navigate to localhost/register/ to register as either a teacher or a student.

User Login: Navigate to localhost/login/ to log in.

Dashboard:

If logged in as a teacher, you will see your details.

If logged in as a student, you will see which teacher is assigned to you.

JWT Authentication is used for secure login sessions.

PostgreSQL is set up with environment variables for secure database management.

Installation

1. Clone the Repository

git clone https://github.com/divyanshi0088/project_destm.git


cd project_destm

2. Install Dependencies

pip install -r requirements.txt

3. Database Setup

Make sure you have PostgreSQL installed and running. Update the .env file with your database credentials.

4. Run Migrations

python manage.py migrate

5. Create a Superuser (Optional)

python manage.py createsuperuser

6. Run the Development Server

python manage.py runserver

Navigate to http://localhost:8000/ to access the project.


Usage

Register a User

Go to localhost/register/

Choose Teacher or Student

Submit the form to create an account

Log In

Go to localhost/login/

Enter your credentials

You will be redirected to the dashboard

Dashboard Access

Teacher: Can view their details

Student: Needs an assigned teacher to access details

Technologies Used

Django Rest Framework (DRF)

PostgreSQL (with environment variable setup)

JWT Authentication

HTML, CSS, JavaScript for frontend

