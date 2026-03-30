from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from auth.models import User
from properties.models import Property
from .models import SavedProperty

saved_bp = Blueprint("saved", __name__, url_prefix="/api/saved")

@saved_bp.route("/<int:property_id>", methods=["POST"])
@jwt_required()
def save_property(property_id):
    user_id = get_jwt_identity()

    exists = SavedProperty.query.filter_by(
        user_id=user_id,
        property_id=property_id
    ).first()

    if not exists:
        db.session.add(
            SavedProperty(user_id=user_id, property_id=property_id)
        )
        db.session.commit()

    return jsonify({"message": "saved"}), 200


@saved_bp.route("/<int:property_id>", methods=["DELETE"])
@jwt_required()
def unsave_property(property_id):
    user_id = get_jwt_identity()

    SavedProperty.query.filter_by(
        user_id=user_id,
        property_id=property_id
    ).delete()

    db.session.commit()
    return jsonify({"message": "unsaved"}), 200


@saved_bp.route("", methods=["GET"])
@jwt_required()
def get_saved_properties():
    user_id = get_jwt_identity()

    saved = (
        Property.query
        .join(SavedProperty, Property.id == SavedProperty.property_id)
        .filter(SavedProperty.user_id == user_id)
        .all()
    )

    return jsonify([p.to_dict() for p in saved]), 200
