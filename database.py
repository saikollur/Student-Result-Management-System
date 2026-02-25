import sqlite3

def get_connection():
    conn = sqlite3.connect('student.db')
    #usually sql queries return in tuples, this makes them to return as a dictionary
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    #cursor is used to run sql statements
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            marks INTEGER NOT NULL,
            grade TEXT NOT NULL
        )
    ''')

    #saves changes to db
    conn.commit()
    conn.close()

def add_student(roll_no, name, marks, grade):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO students (roll_no, name, marks, grade)
        VALUES (?, ?, ?, ?)
    ''', (roll_no, name, marks, grade))

    conn.commit()
    conn.close()

def get_students():
    conn = get_connected()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Students')
    #collects all the results into a list.
    students = cursor.fetchall()

    conn.close()
    return students

def search_student(roll_no):
    conn = get_connection
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM students WHERE roll_no = ?', (roll_no,))
    student = cursor.fetchone

    conn.close()
    return student


