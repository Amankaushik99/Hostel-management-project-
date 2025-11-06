from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql
from datetime import datetime, date
import sys
from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Database Configuration from environment variables
DB_CONFIG = Config.DB_CONFIG

def get_db_connection():
    conn = pymysql.connect(**DB_CONFIG)
    conn.cursorclass = pymysql.cursors.DictCursor
    return conn

def check_database():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM students")
        cursor.fetchone()
        conn.close()
        print("✅ Database connection successful!")
        return True
    except pymysql.Error as e:
        if "doesn't exist" in str(e) or "Unknown database" in str(e):
            print("\n❌ ERROR: Database or tables don't exist!")
            print("🚨 Run: mysql -u root -p < database.sql")
        else:
            print(f"\n❌ Database error: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM students WHERE student_id = %s AND password = %s', 
                      (user_id, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['student_id']
            session['user_type'] = 'student'
            session['user_name'] = user['name']
            conn.close()
            return redirect(url_for('student_dashboard'))
        
        conn.close()
        flash('Invalid student credentials!')
    
    return render_template('student_login.html')

@app.route('/faculty_login', methods=['GET', 'POST'])
def faculty_login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM faculty WHERE faculty_id = %s AND password = %s', 
                      (user_id, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['faculty_id']
            session['user_type'] = 'faculty'
            session['user_name'] = user['name']
            conn.close()
            return redirect(url_for('faculty_dashboard'))
        
        conn.close()
        flash('Invalid faculty credentials!')
    
    return render_template('faculty_login.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM admin WHERE admin_id = %s AND password = %s', 
                      (user_id, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['admin_id']
            session['user_type'] = 'admin'
            session['user_name'] = user['name']
            conn.close()
            return redirect(url_for('admin_dashboard'))
        
        conn.close()
        flash('Invalid admin credentials!')
    
    return render_template('admin_login.html')

# Keep the old login route for backward compatibility, redirect to student login
@app.route('/login')
def login():
    return redirect(url_for('student_login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''INSERT INTO students (student_id, name, room_number, phone, email, password)
                           VALUES (%s, %s, %s, %s, %s, %s)''',
                       (request.form['student_id'], request.form['name'], 
                        request.form['room_number'], request.form['phone'],
                        request.form['email'], request.form['password']))
            conn.commit()
            flash('Student registered successfully!')
            return redirect(url_for('student_login'))
        except pymysql.IntegrityError:
            flash('Student ID already exists!')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/student_dashboard')
def student_dashboard():
    if 'user_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('student_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''SELECT * FROM pass_requests 
                     WHERE student_id = %s 
                     ORDER BY request_date DESC''', 
                   (session['user_id'],))
    pass_requests = cursor.fetchall()
    
    today = date.today()
    cursor.execute('''SELECT * FROM attendance 
                     WHERE student_id = %s AND date = %s''', 
                   (session['user_id'], today))
    attendance = cursor.fetchone()
    
    conn.close()
    return render_template('student_dashboard.html', 
                         pass_requests=pass_requests, 
                         attendance=attendance)

@app.route('/faculty_dashboard')
def faculty_dashboard():
    if 'user_id' not in session or session['user_type'] != 'faculty':
        return redirect(url_for('faculty_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''SELECT pr.*, s.name, s.room_number 
                     FROM pass_requests pr 
                     JOIN students s ON pr.student_id = s.student_id 
                     WHERE pr.status = 'pending' 
                     ORDER BY pr.request_date DESC''')
    pending_requests = cursor.fetchall()
    
    today = date.today()
    cursor.execute('''SELECT s.student_id, s.name, s.room_number,
                     a.check_in_time, a.check_out_time, a.status
                     FROM students s
                     LEFT JOIN attendance a ON s.student_id = a.student_id 
                     AND a.date = %s
                     ORDER BY s.room_number''', (today,))
    attendance_summary = cursor.fetchall()
    
    conn.close()
    return render_template('faculty_dashboard.html', 
                         pending_requests=pending_requests,
                         attendance_summary=attendance_summary)

@app.route('/request_pass', methods=['GET', 'POST'])
def request_pass():
    if 'user_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('student_login'))
    
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO pass_requests (student_id, leave_type, reason, from_date, to_date)
                       VALUES (%s, %s, %s, %s, %s)''',
                   (session['user_id'], request.form['leave_type'], request.form['reason'],
                    request.form['from_date'], request.form['to_date']))
        conn.commit()
        conn.close()
        flash('Pass request submitted successfully!')
        return redirect(url_for('student_dashboard'))
    
    return render_template('request_pass.html')

@app.route('/mark_attendance')
def mark_attendance():
    if 'user_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('student_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    today = date.today()
    now = datetime.now()
    
    cursor.execute('''SELECT * FROM attendance 
                     WHERE student_id = %s AND date = %s''', 
                   (session['user_id'], today))
    existing = cursor.fetchone()
    
    if existing:
        if existing['check_out_time'] is None:
            cursor.execute('''UPDATE attendance 
                           SET check_out_time = %s 
                           WHERE student_id = %s AND date = %s''',
                       (now, session['user_id'], today))
            flash('Check-out marked successfully!')
        else:
            flash('Attendance already completed for today!')
    else:
        cursor.execute('''INSERT INTO attendance (student_id, date, check_in_time)
                       VALUES (%s, %s, %s)''',
                   (session['user_id'], today, now))
        flash('Check-in marked successfully!')
    
    conn.commit()
    conn.close()
    return redirect(url_for('student_dashboard'))

@app.route('/approve_pass/<int:request_id>/<action>')
def approve_pass(request_id, action):
    if 'user_id' not in session or session['user_type'] != 'faculty':
        return redirect(url_for('faculty_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    status = 'approved' if action == 'approve' else 'rejected'
    
    cursor.execute('''UPDATE pass_requests 
                   SET status = %s, approved_by = %s 
                   WHERE id = %s''',
               (status, session['user_id'], request_id))
    conn.commit()
    conn.close()
    
    flash(f'Pass request {status} successfully!')
    return redirect(url_for('faculty_dashboard'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get counts for dashboard
    cursor.execute('SELECT COUNT(*) as count FROM students')
    student_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM faculty')
    faculty_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM pass_requests WHERE status = "pending"')
    pending_requests = cursor.fetchone()['count']
    
    conn.close()
    return render_template('admin_dashboard.html', 
                         student_count=student_count,
                         faculty_count=faculty_count,
                         pending_requests=pending_requests)

@app.route('/admin_profile')
def admin_profile():
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admin WHERE admin_id = %s', (session['user_id'],))
    admin = cursor.fetchone()
    conn.close()
    
    return render_template('admin_profile.html', admin=admin)

@app.route('/faculty_profile')
def faculty_profile():
    if 'user_id' not in session or session['user_type'] != 'faculty':
        return redirect(url_for('faculty_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM faculty WHERE faculty_id = %s', (session['user_id'],))
    faculty = cursor.fetchone()
    conn.close()
    
    return render_template('faculty_profile.html', faculty=faculty)

@app.route('/manage_students')
def manage_students():
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students ORDER BY student_id')
    students = cursor.fetchall()
    conn.close()
    
    return render_template('manage_students.html', students=students)

@app.route('/manage_faculty')
def manage_faculty():
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM faculty ORDER BY faculty_id')
    faculty = cursor.fetchall()
    conn.close()
    
    return render_template('manage_faculty.html', faculty=faculty)

@app.route('/add_faculty', methods=['GET', 'POST'])
def add_faculty():
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO faculty (faculty_id, name, department, password)
                           VALUES (%s, %s, %s, %s)''',
                       (request.form['faculty_id'], request.form['name'],
                        request.form['department'], request.form['password']))
            conn.commit()
            flash('Faculty added successfully!')
            return redirect(url_for('manage_faculty'))
        except pymysql.IntegrityError:
            flash('Faculty ID already exists!')
        finally:
            conn.close()
    
    return render_template('add_faculty.html')

@app.route('/edit_student/<student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        cursor.execute('''UPDATE students 
                       SET name = %s, room_number = %s, phone = %s, email = %s
                       WHERE student_id = %s''',
                   (request.form['name'], request.form['room_number'],
                    request.form['phone'], request.form['email'], student_id))
        conn.commit()
        conn.close()
        flash('Student updated successfully!')
        return redirect(url_for('manage_students'))
    
    cursor.execute('SELECT * FROM students WHERE student_id = %s', (student_id,))
    student = cursor.fetchone()
    conn.close()
    
    return render_template('edit_student.html', student=student)

@app.route('/delete_student/<student_id>')
def delete_student(student_id):
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Delete related records first
    cursor.execute('DELETE FROM attendance WHERE student_id = %s', (student_id,))
    cursor.execute('DELETE FROM pass_requests WHERE student_id = %s', (student_id,))
    cursor.execute('DELETE FROM students WHERE student_id = %s', (student_id,))
    
    conn.commit()
    conn.close()
    flash('Student deleted permanently!')
    return redirect(url_for('manage_students'))

@app.route('/edit_faculty/<faculty_id>', methods=['GET', 'POST'])
def edit_faculty(faculty_id):
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        cursor.execute('''UPDATE faculty 
                       SET name = %s, department = %s
                       WHERE faculty_id = %s''',
                   (request.form['name'], request.form['department'], faculty_id))
        conn.commit()
        conn.close()
        flash('Faculty updated successfully!')
        return redirect(url_for('manage_faculty'))
    
    cursor.execute('SELECT * FROM faculty WHERE faculty_id = %s', (faculty_id,))
    faculty = cursor.fetchone()
    conn.close()
    
    return render_template('edit_faculty.html', faculty=faculty)

@app.route('/delete_faculty/<faculty_id>')
def delete_faculty(faculty_id):
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM faculty WHERE faculty_id = %s', (faculty_id,))
    conn.commit()
    conn.close()
    flash('Faculty removed successfully!')
    return redirect(url_for('manage_faculty'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("🏨 Hostel Management System")
    print("=" * 40)
    
    if '--skip-db-check' not in sys.argv and not Config.SKIP_DB_CHECK:
        if not check_database():
            print("\n🚨 APPLICATION CANNOT START!")
            print("📋 Run: mysql -u root -p < database.sql")
            exit(1)
    
    print("🚀 Starting application...")
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)