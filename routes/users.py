from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    jsonify,
)
from database.db import students_collection, professors_collection, subjects_collection
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

users = Blueprint("users", __name__)


@users.route("/")
def home():
    return render_template("index.html")


#! Registration Form
@users.route("/submit", methods=["POST"])
def submit():
    first_name = request.form.get("first_name").strip().upper()
    last_name = request.form.get("last_name").strip().upper()
    id_number = request.form.get("id_number").strip().upper()
    is_student = request.form.get("is_student") == "true"
    email = request.form.get("email").strip().lower()
    password = generate_password_hash(request.form.get("password"))

    existing_student = students_collection.find_one({"id_number": id_number})
    existing_professor = professors_collection.find_one({"id_number": id_number})
    existing_student_email = students_collection.find_one({"email": email})
    existing_professor_email = professors_collection.find_one({"email": email})

    if existing_student or existing_professor:
        return (
            jsonify({"success": False, "message": "ID number is already registered."}),
            409,
        )

    if existing_student_email or existing_professor_email:
        return (
            jsonify({"success": False, "message": "Email is already registered."}),
            409,
        )

    user = {
        "first_name": first_name,
        "last_name": last_name,
        "id_number": id_number,
        "email": email,
        "password": password,
    }

    if is_student:
        user["program"] = request.form.get("program")
        user["year_level"] = request.form.get("year_level")
        user["section"] = request.form.get("section")

        result = students_collection.insert_one(user)
        session["role"] = "student"
    else:
        result = professors_collection.insert_one(user)
        session["role"] = "professor"

    session["user_id"] = str(result.inserted_id)
    return jsonify({"success": True, "message": "Success! Directing to overview."})


#! Login Form
@users.route("/login", methods=["POST"])
def login():
    id_number = request.form.get("id_number", "").strip().upper()
    password = request.form.get("password", "")

    user = students_collection.find_one({"id_number": id_number})
    role = "student"

    if not user:
        user = professors_collection.find_one({"id_number": id_number})
        role = "professor"

    if user and check_password_hash(user["password"], password):
        session["user_id"] = str(user["_id"])
        session["id_number"] = user["id_number"]
        session["role"] = role

        return jsonify(
            {"success": True, "message": "Login successful! Redirecting to overview."}
        )

    return jsonify({"success": False, "message": "Invalid ID number or password."}), 401


#! Dashboard
@users.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("users.home"))

    from bson import ObjectId

    user_id = ObjectId(session["user_id"])

    if session.get("role") == "student":
        user = students_collection.find_one({"_id": user_id})
    else:
        user = professors_collection.find_one({"_id": user_id})

    subjects = list(subjects_collection.find())

    days = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }

    now = datetime.now()

    def get_next_class(subject):
        subject_day = days.get(subject.get("schedule"))

        if subject_day is None:
            return datetime.max

        try:
            subject_time = datetime.strptime(subject.get("time", ""), "%H:%M").time()
        except ValueError:
            return datetime.max

        days_until = (subject_day - now.weekday()) % 7

        next_class = datetime.combine(
            now.date() + timedelta(days=days_until), subject_time
        )

        if next_class <= now:
            next_class += timedelta(days=7)

        return next_class

    upcoming_subjects = sorted(subjects, key=get_next_class)

    return render_template(
        "overview_block.html",
        first_name=user["first_name"],
        page_title="Overview",
        subjects=subjects,
        upcoming_subjects=upcoming_subjects,
        now=now,
    )


# TODO Add subjects testing
@users.route("/testing_subjects", methods=["POST"])
def testing_subjects():
    subject = {
        "subject_code": request.form.get("subject_code", "").strip().upper(),
        "subject_name": request.form.get("subject_name", "").strip(),
        "schedule": request.form.get("schedule", "").strip(),
        "time": request.form.get("time", "").strip(),
        "room": request.form.get("room", "").strip(),
        "student_count": int(request.form.get("student_count", 0)),
    }

    subjects_collection.insert_one(subject)

    return redirect(url_for("users.dashboard"))


@users.route("/subjects_route")
def subjects_route():
    return render_template("test_add_subjects.html")


@users.route("/attendance")
def attendance():
    if "user_id" not in session:
        return redirect(url_for("users.home"))

    return render_template("attendance_block.html")


@users.route("/student/profile")
def student_profile():
    return render_template("student_profile.html")


@users.route("/settings")
def settings():
    return render_template("settings.html")


@users.route("/student/overview")
def student_overview():
    return render_template("student/overview.html")
