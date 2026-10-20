import os
from dotenv import load_dotenv

load_dotenv()
print("-> DEBUG: MONGO_URI is currently:", os.getenv("MONGO_URI"))

from flask import Flask
from routes.users import users
from routes.subjects import subjects_bp
from routes.admin import admin_bp
from routes.students import students_bp

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "attendance_secret_key2026"
)

app.register_blueprint(users)
app.register_blueprint(subjects_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(students_bp)

if __name__ == "__main__":
    app.run(debug=True)