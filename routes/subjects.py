from flask import Blueprint, render_template, request, redirect, url_for, session
from database.db import db

subjects_bp = Blueprint('subjects', __name__)

@subjects_bp.route('/subjects', methods=['GET'])
def subjects():
    all_subjects = list(db.subjects.find({}))
    return render_template('subjects.html', subjects=all_subjects)

@subjects_bp.route('/add-subject', methods=['GET', 'POST'])
def add_subject():
    if request.method == 'POST':
        subject_code = request.form.get('code')
        subject_name = request.form.get('name')
        instructor = request.form.get('instructor')
        schedule = request.form.get('schedule')
        room = request.form.get('room')
        
        db.subjects.insert_one({
            "code": subject_code,
            "name": subject_name,
            "instructor": instructor,
            "schedule": schedule,
            "room": room
        })
        return redirect(url_for('subjects.subjects'))
        
    return render_template('test_add_subjects.html')