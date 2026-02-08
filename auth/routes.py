from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from db import db
from .models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

bcrypt = Bcrypt()


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify(error="Missing username or password"), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify(error="Username already exists"), 409

    hashed_password = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    new_user = User(
        username=data["username"],
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="User registered successfully"), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify(error="Missing username or password"), 400

    user = User.query.filter_by(username=data["username"]).first()

    if not user:
        return jsonify(error="Invalid credentials"), 401

    if not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify(error="Invalid credentials"), 401

    access_token = create_access_token(identity=str(user.id))




    return jsonify(access_token=access_token), 200


@auth_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    return jsonify(
        message="You are authenticated",
        user_id=user_id
    ), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())  # convert back
    user = User.query.get(user_id)

    return jsonify(
        id=user.id,
        username=user.username
    ), 200
