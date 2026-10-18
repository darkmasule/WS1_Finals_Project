from flask import Blueprint, render_template, request, session, redirect, url_for
from database.db import students_collection, professors_collection
from werkzeug.security import generate_password_hash, check_password_hash

users = Blueprint("users", __name__)


@users.route("/")
def home():
    return render_template("index.html")


#! Registration Form
@users.route("/submit", methods=["POST"])
def submit():
    first_name = request.form.get("first_name").strip().upper()
    last_name = request.form.get("last_name").strip().upper()
    id_number = request.form.get("id_number").strip()
    is_student = request.form.get("is_student") == "true"
    email = request.form.get("email").strip()
    password = generate_password_hash(request.form.get("password"))

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

        students_collection.insert_one(user)

    else:
        professors_collection.insert_one(user)

    return """ <h1>Submitted Successfully!</h1>
    <a href="/">Back to Form</a> """


#! Login Form
@users.route("/login", methods=["POST"])
def login():
    id_number = request.form.get("id_number", "").strip()
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

        return redirect(url_for("users.dashboard"))

    return "Invalid ID number or password"


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

    return render_template("overview_block.html", first_name=user["first_name"])


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
