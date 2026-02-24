from flask import Flask
from database import init_db

app = Flask(__name__)

with app.app_context():
    init_db()

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
