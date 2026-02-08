from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from db import db
from auth.routes import auth_bp
from auth.models import User  # ensures table creation

# --------------------
# App setup
# --------------------
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "change-this-secret-key"

db.init_app(app)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)

# --------------------
# Register blueprints
# --------------------
app.register_blueprint(auth_bp)

# --------------------
# App entry
# --------------------

print(app.url_map)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


