from flask import Flask, request, redirect, url_for, render_template
from database import init_db, add_student, get_students, search_student, update_student, delete_student, calculate_grade, get_student_count

app = Flask(__name__)

#whenever we restart this gives the webserver context
with app.app_context():
    init_db()

# this is a decorator
@app.route('/')
def home():
    count = get_student_count()
    return render_template('index.html', count = count)

@app.route('/add', methods=['GET', 'POST'])
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
def delete_student_route(roll_no):
    student = search_student(roll_no)

    if not student:
        return render_template('error.html', message=f'No student found with Roll No: {roll_no}')

    delete_student(roll_no)
    return redirect(url_for('view_students'))

if __name__ == "__main__":
    app.run(debug=True)
