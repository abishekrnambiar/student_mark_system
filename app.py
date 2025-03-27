from flask import Flask, request, render_template, session, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",  # Replace with your MySQL password
    database="your_database_name"
)

# Generate unique username based on first name
def generate_username(first_name):
    with db.cursor() as cursor:
        base_username = first_name.lower()
        cursor.execute("SELECT username FROM Users WHERE username = %s", (base_username,))
        if not cursor.fetchone():
            return base_username
        i = 1
        while True:
            new_username = f"{base_username}{i}"
            cursor.execute("SELECT username FROM Users WHERE username = %s", (new_username,))
            if not cursor.fetchone():
                return new_username
            i += 1

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM Users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
    if user:
        session['username'] = user['username']
        session['role'] = user['role']
        if user['role'] == 'teacher':
            return redirect(url_for('teacher_main'))
        elif user['role'] == 'student':
            return redirect(url_for('student_dashboard', first_login=not user['password_changed']))
    return render_template('login_error.html')  # Render error template instead of plain text

# Rest of your routes remain unchanged...
@app.route('/teacher')
def teacher_main():
    if session.get('role') != 'teacher':
        return "Unauthorized!"
    return render_template('teacher_main.html')

@app.route('/student_details')
def student_details():
    if session.get('role') != 'teacher':
        return "Unauthorized!"
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT u.username, s.name, s.department FROM Students s JOIN Users u ON s.username = u.username ORDER BY u.username")
        students = cursor.fetchall()
    return render_template('student_details.html', students=students)

@app.route('/subject_marks')
def subject_marks():
    if session.get('role') != 'teacher':
        return "Unauthorized!"
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT u.username, s.name, s.department, g.grade_id, g.subject, g.mark " +
                       "FROM Students s JOIN Users u ON s.username = u.username " +
                       "LEFT JOIN Grades g ON u.username = g.username ORDER BY u.username")
        rows = cursor.fetchall()
    students_dict = {}
    for row in rows:
        username = row['username']
        if username not in students_dict:
            students_dict[username] = {'name': row['name'], 'department': row['department'], 'grades': [], 'total': 0}
        if row['grade_id']:
            students_dict[username]['grades'].append({'grade_id': row['grade_id'], 'subject': row['subject'], 'mark': row['mark']})
            if row['mark'] is not None:
                students_dict[username]['total'] += row['mark']
    students = [{'username': k, **v} for k, v in students_dict.items()]
    return render_template('subject_marks.html', students=students)

@app.route('/student')
def student_dashboard():
    if session.get('role') != 'student':
        return "Unauthorized!"
    first_login = request.args.get('first_login', default='False') == 'True'
    username = session['username']
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT name, department FROM Students WHERE username = %s", (username,))
        student = cursor.fetchone()
        cursor.execute("SELECT subject, mark FROM Grades WHERE username = %s", (username,))
        grades = cursor.fetchall()
    total_marks = sum(grade['mark'] for grade in grades if grade['mark'] is not None)
    return render_template('student.html', student=student, grades=grades, total_marks=total_marks, first_login=first_login)

@app.route('/add_student', methods=['POST'])
def add_student():
    if session.get('role') != 'teacher':
        return "Unauthorized!"
    name = request.form['name']
    department = request.form['department']
    first_name = name.split()[0]
    username = generate_username(first_name)
    with db.cursor() as cursor:
        cursor.execute("INSERT INTO Users (username, password, role, password_changed) VALUES (%s, %s, 'student', FALSE)", 
                       (username, first_name.lower()))
        cursor.execute("INSERT INTO Students (username, name, department) VALUES (%s, %s, %s)", 
                       (username, name, department))
        db.commit()
    return redirect(url_for('student_details'))

@app.route('/check_username', methods=['POST'])
def check_username():
    data = request.get_json()
    username = data.get('username')
    with db.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM Students WHERE username = %s", (username,))
        count = cursor.fetchone()[0]
    return jsonify({"exists": count > 0})

@app.route('/add_grade', methods=['POST'])
def add_grade():
    if session.get('role') != 'teacher':
        return "Unauthorized!"
    username = request.form['username']
    subject = request.form['subject']
    mark = int(request.form['mark'])
    with db.cursor() as cursor:
        cursor.execute("INSERT INTO Grades (username, subject, mark) VALUES (%s, %s, %s)", (username, subject, mark))
        db.commit()
    return redirect(url_for('subject_marks'))

@app.route('/edit_grade', methods=['POST'])
def edit_grade():
    if session.get('role') != 'teacher':
        return "Unauthorized!"
    grade_id = request.form['grade_id']
    new_mark = int(request.form['mark'])
    with db.cursor() as cursor:
        cursor.execute("UPDATE Grades SET mark = %s WHERE grade_id = %s", (new_mark, grade_id))
        db.commit()
    return redirect(url_for('subject_marks'))

@app.route('/delete_grade', methods=['POST'])
def delete_grade():
    if session.get('role') != 'teacher':
        return "Unauthorized!"
    grade_id = request.form['grade_id']
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM Grades WHERE grade_id = %s", (grade_id,))
        db.commit()
    return redirect(url_for('subject_marks'))

@app.route('/edit_department', methods=['POST'])
def edit_department():
    if session.get('role') != 'teacher':
        return "Unauthorized!"
    username = request.form['username']
    new_department = request.form['department']
    with db.cursor() as cursor:
        cursor.execute("UPDATE Students SET department = %s WHERE username = %s", (new_department, username))
        db.commit()
    return redirect(url_for('student_details'))

@app.route('/delete_student', methods=['POST'])
def delete_student():
    if session.get('role') != 'teacher':
        return "Unauthorized!"
    username = request.form['username']
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM Grades WHERE username = %s", (username,))
        cursor.execute("DELETE FROM Students WHERE username = %s", (username,))
        cursor.execute("DELETE FROM Users WHERE username = %s", (username,))
        db.commit()
    return redirect(url_for('student_details'))

@app.route('/change_password', methods=['POST'])
def change_password():
    if session.get('role') != 'student':
        return "Unauthorized!"
    new_password = request.form['new_password']
    username = session['username']
    with db.cursor() as cursor:
        cursor.execute("UPDATE Users SET password = %s, password_changed = TRUE WHERE username = %s", 
                       (new_password, username))
        db.commit()
    session.clear()
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)