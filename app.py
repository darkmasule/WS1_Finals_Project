import os
from dotenv import load_dotenv
from flask import Flask
from routes.users import users

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

app.register_blueprint(users)

if __name__ == "__main__":
    app.run(debug=True)
