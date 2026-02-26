import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, 'students.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    #usually sql queries return in tuples, this makes them to return as a dictionary
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    #cursor is used to run sql statements
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students(
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
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM students')
    #collects all the results into a list.
    students = cursor.fetchall()

    conn.close()
    return students

def search_student(roll_no):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM students WHERE roll_no = ?', (roll_no,))
    student = cursor.fetchone()

    conn.close()
    return student

def update_student(roll_no, name, marks, grade):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''
        UPDATE students
        SET name = ?, marks = ?, grade = ?
        WHERE roll_no = ?
    ''', (name, marks, grade, roll_no))

    conn.commit()
    conn.close()

def delete_student(roll_no):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE From students WHERE roll_no = ?', (roll_no,))

    conn.commit()
    conn.close()
