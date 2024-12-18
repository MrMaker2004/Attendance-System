from flask import jsonify
from flask import Flask, render_template, redirect, url_for, session, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from extensions import db  # Import the single db instance
import os
from models import User, Attendance, Course, Marks, Test  # Import all models
# from models import Attendance, Course, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a0f0d5a116e1e6b03e394451f2b7476c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin81:admin81@localhost/attendance_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'index'

# Import models here AFTER db.init_app()
with app.app_context():
    db.create_all()


# Import Models




@login_manager.user_loader
def load_user(user_id):
    try:
        rno, branch, sem = user_id.split('|')
        return User.query.filter_by(Rno=rno, Branch=branch, Sem=sem).first()
    except ValueError:
        return None

# Routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(Username=username).first()
    if user and user.Password == password:
        login_user(user)
        return jsonify({'redirect': url_for('dashboard')})
    return "Invalid credentials", 401

from flask import render_template
from app import db
from models import Attendance, Course  # Import your models

# ...existing code...

# ...existing imports...

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = current_user.get_id()
    rno, branch, sem = user_id.split('|')

    # Retrieve attendance records joined with course information
    attendance_records = (
        db.session.query(Attendance, Course)
        .join(Course, Attendance.CId == Course.CId)
        .filter(
            Attendance.Rno == rno,
            Attendance.Branch == branch,
            Attendance.Sem == sem
        )
        .all()
    )

    # Extract course names and attendance percentages
    courses = [record.Course.Cname for record in attendance_records]
    attendance_data = [record.Attendance.Attendance_perc for record in attendance_records]

    # Calculate total attended classes and total classes
    total_attended = sum(record.Attendance.Attended for record in attendance_records)
    total_classes = sum(record.Attendance.Classes for record in attendance_records)

    # Calculate overall attendance percentage
    overall_percentage = (total_attended / total_classes) * 100 if total_classes > 0 else 0

    # Pass variables to the template
    return render_template(
        'dashboard.html',
        overall_percentage=overall_percentage,
        courses=courses,
        attendance_data=attendance_data
    )
# ...existing code...

@app.route('/attendance/<semester>')
@login_required
def attendance_page(semester):
    if semester not in ['odd', 'even']:
        return "Invalid semester", 400

    user_id = current_user.get_id()
    rno, branch = user_id.split('|')[:2]  # Assuming user ID contains details

    # Define semester mapping: Odd semesters = 1, 3 | Even semesters = 2
    semester_filter = [1, 3] if semester == 'odd' else [2]

    # Query attendance based on Rno, Branch, and semester
    attendance_records = Attendance.query.filter_by(Rno=rno, Branch=branch).filter(
        Attendance.Sem.in_(semester_filter)
    ).all()

    # Prepare data for the template
    data = [
        {
            'course': record.course.Cname if record.course else 'N/A',
            'classes': record.Classes,
            'attended': record.Attended,
            'percentage': record.Attendance_perc
        }
        for record in attendance_records
    ]

    return render_template('attendance.html', semester=semester, data=data)


@app.route('/marks/<semester>')
@login_required
def marks_page(semester):
    if semester not in ['odd', 'even']:
        return "Invalid semester", 400
    return render_template('marks.html', semester=semester)

@app.route('/profile')
@login_required
def profile_page():
    user = current_user
    return render_template('profile.html', user=user)

@app.route('/announcements')
@login_required
def announcements_page():
    user = current_user
    return render_template('announcements.html', user=user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)
