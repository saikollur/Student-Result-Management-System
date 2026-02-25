from flask import Flask, request, redirect, url_for, render_template
from database import init_db, add_student, get_students, search_student

app = Flask(__name__)

#whenever we restart this gives the webserver context
with app.app_context():
    init_db()

# this is a decorator
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    message = ''
    if request.method == 'POST':
        roll_no = request.form['roll_no'].strip()
        name = request.form['name'].strip()
        marks = request.form['marks'].strip()
        grade = request.form['grade'].strip()

        if not roll_no or not name or not marks or not grade:
            message = 'All fields are required!'
        elif not marks.isdigit() or not (0 <= int(marks) <= 100):
            message = 'Marks must be a number between 0 and 100!'
        else :
            try:
                add_student(roll_no, name, int(marks), grade)
                message = 'Student added successfully!'
            except Exception as e:
                message = f'Error: Roll number already exists'
    return render_template('add_student.html', message = message)

@app.route('/view')
def view_students():
    students = get_all_students()
    return render_template('view_students.html', students = students)

@app.route('/search', methods=['GET', 'POST'])
def search():
    student = None
    message = ''

    if request.methods == 'POST':
        roll_no = request.form['roll_no'].strip()

        if not roll_no:
            message = 'Please enter a roll number!'
        else:
            student = search_student(roll_no)
            if not student:
                message = f'No student found with Roll No: {roll_no}'

    return render_template('search.html', message=message)
    
if __name__ == "__main__":
    app.run(debug=True)
