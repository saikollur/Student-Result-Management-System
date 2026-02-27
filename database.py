import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
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

def calculate_grade(marks):
    if marks >= 90:
        return 'A+'
    elif marks >= 80:
        return 'A'
    elif marks >= 70:
        return 'B'
    elif marks >= 60:
        return 'C'
    elif marks >= 50:
        return 'D'
    else:
        return 'F'

def get_student_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM students')
    count = cursor.fetchone()[0]

    conn.close()
    return count

def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    hashed = generate_password_hash(password)

    cursor.execute('''
        INSERT INTO users (username, password)
        VALUES (?, ?)
    ''', (username, hashed))

    conn.commit()
    conn.close()

def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    conn.close()
    return user

def check_username_exists(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    exists = cursor.fetchone()

    conn.close()
    return exists is not None

def verify_password(username, password):
    user = get_user(username)
    if not user:
        return False
    return check_password_hash(user['password'], password)

