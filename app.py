# app.py
from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app =Flask(__name__, static_folder='frontend/static', template_folder='frontend/templates')


def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    
    # Create students table
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER UNIQUE NOT NULL,
            Name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            year INTEGER NOT NULL,
            photo BLOB
        ) 
    ''')
    
    # Create courses table
    c.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            course_code TEXT UNIQUE NOT NULL,
            instructor TEXT NOT NULL
        )
    ''')
    
    # Create enrollments table (many-to-many relationship)
    c.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            student_id INTEGER,
            course_id INTEGER,
            enrollment_date DATE DEFAULT CURRENT_DATE,
            grade FLOAT,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (course_id) REFERENCES courses (id),
            PRIMARY KEY (student_id, course_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/api_students', methods=['GET'])
def get_students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('SELECT * FROM students')
    students = c.fetchall()
    conn.close()
    
    return jsonify([{
        'studentiId': s[0],
        'studentName': s[1],
        'studentEmail': s[2],
        'studentDepartment': s[3],
        'studentYear': s[4],
        'studentPhoto': s[5]
    } for s in students])

@app.route('/api_students', methods=['POST'])
def add_student():
    data = request.json
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    
    try:
        c.execute('''
            INSERT INTO students (id ,name, email, department, year, photo)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['studentId'],
            data['studentName'],
            data['studentEmail'],
            data['studentDepartment'],
            data['studentYear'],
            data['studentPhoto']
        ))
        conn.commit()
        return jsonify({'success': True, 'message': 'Student added successfully'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Email already exists'}), 400
    finally:
        conn.close()

