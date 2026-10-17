import os
from flask import Flask
from routes.users import users

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "attendance_secret_key2026")

app.register_blueprint(users)

if __name__ == "__main__":
    app.run(debug=True)
