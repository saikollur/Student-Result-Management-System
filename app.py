from flask import Flask

app = Flask(__name__)

# this is a decorator
@app.route('/')
def home():
    return 'Student Result Management System'

@app.route('/add')
def add_student():
    return 'This is the Add Student page'

@app.route('/view')
def view_student():
    return 'This is the View Student page'

if __name__ == "__main__":
    app.run(debug=True)
