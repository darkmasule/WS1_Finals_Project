from flask import Blueprint, render_template
from database.db import db

students_bp = Blueprint('student_bp', __name__)

@students_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@students_bp.route('/student/profile', methods=['GET'])
def student_profile():
    return render_template('student_profile.html')

@students_bp.route('/student/account', methods=['GET'])
def student_account():
    return render_template('student_accountprofile.html')

@students_bp.route('/student/history', methods=['GET'])
def student_attendance_history():
    return render_template('student_attendance_history.html')

@students_bp.route('/credentials', methods=['GET'])
def user_credentials():
    return render_template('user_credentials.html')

@students_bp.route('/dasc', methods=['GET'])
def dasc():
    return render_template('dasc.html')

@students_bp.route('/test/subjects', methods=['GET'])
def test_add_subjects():
    return render_template('test_add_subjects.html')