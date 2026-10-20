from flask import Blueprint, render_template
from database.db import db

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin/overview', methods=['GET'])
def admin_overview():
    return render_template('admin/admin_overview.html')

@admin_bp.route('/admin/students', methods=['GET'])
def admin_students():
    students_list = list(db.students.find({}))
    return render_template('admin_students.html', students=students_list)

@admin_bp.route('/admin/attendance', methods=['GET'])
def admin_attendance():
    logs_list = list(db.attendance.find({}).sort("timestamp", -1))
    return render_template('admin_attendance.html', logs=logs_list)

@admin_bp.route('/admin/vetting', methods=['GET'])
def admin_vetting():
    return render_template('admin_vetting.html')

@admin_bp.route('/admin/settings', methods=['GET'])
def admin_settings():
    return render_template('admin_settings.html')