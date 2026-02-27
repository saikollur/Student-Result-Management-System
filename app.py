from flask import Flask, request, redirect, url_for, render_template, session
from database import (init_db, add_student, get_students, search_student,
                      update_student, delete_student, calculate_grade,
                      get_student_count, register_user, verify_password,
                      check_username_exists)
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
#whenever we restart this gives the webserver context
with app.app_context():
    init_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        confirm = request.form['confirm'].strip()

        if not username or not password or not confirm:
            message = 'error:All fields are required!'
        elif len(password) < 6:
            message = 'error:Password must be at least 6 characters!'
        elif password != confirm:
            message = 'error:Passwords do not match!'
        elif check_username_exists(username):
            message = 'error:Username already taken!'
        else:
            register_user(username, password)
            message = 'success:Account created! You can now log in.'

    return render_template('register.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if not username or not password:
            message = 'error:All fields are required!'
        elif verify_password(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            message = 'error:Invalid username or password!'

    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# this is a decorator
@app.route('/')
@login_required
def home():
    count = get_student_count()
    return render_template('index.html', count = count)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_student_route():
    message = ''
    if request.method == 'POST':
        roll_no = request.form['roll_no'].strip()
        name = request.form['name'].strip()
        marks = request.form['marks'].strip()

        if not roll_no or not name or not marks:
            message = 'All fields are required!'
        elif not marks.isdigit() or not (0 <= int(marks) <= 100):
            message = 'Marks must be a number between 0 and 100!'
        else :
            try:
                grade = calculate_grade(int(marks))
                add_student(roll_no, name, int(marks), grade)
                message = 'success:Student added successfully!'
            except Exception as e:
                message = f'Error: Roll number already exists'
    return render_template('add_student.html', message = message)

@app.route('/view')
@login_required
def view_students():
    students = get_students()
    return render_template('view_students.html', students = students)

@app.route('/search', methods=['GET', 'POST'])
def search():
    student = None
    message = ''

    if request.method == 'POST':
        roll_no = request.form['roll_no'].strip()

        if not roll_no:
            message = 'Please enter a roll number!'
        else:
            student = search_student(roll_no)
            if not student:
                message = f'No student found with Roll No: {roll_no}'

    return render_template('search.html', student=student, message=message)

@app.route('/update/<roll_no>', methods=['GET', 'POST'])
@login_required
def update_student_route(roll_no):
    message = ''
    student = search_student(roll_no)

    if not student:
        return render_template('error.html', message=f'No student found with Roll No: {roll_no}')

    if request.method=='POST':
        name  = request.form['name'].strip()
        marks = request.form['marks'].strip()

        if not name or not marks:
            message = 'All fields are required!'
        elif not marks.isdigit() or not (0 <= int(marks) <= 100):
            message = 'Marks must be a number between 0 and 100!'
        else:
            grade = calculate_grade(int(marks))
            update_student(roll_no, name, int(marks), grade)
            return redirect(url_for('view_students'))
    return render_template('update_student.html', student=student, message=message)

@app.route('/delete/<roll_no>')
@login_required
def delete_student_route(roll_no):
    student = search_student(roll_no)

    if not student:
        return render_template('error.html', message=f'No student found with Roll No: {roll_no}')

    delete_student(roll_no)
    return redirect(url_for('view_students'))

if __name__ == "__main__":
    app.run(debug=True)
