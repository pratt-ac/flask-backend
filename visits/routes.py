from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from .models import Visit

visits_bp = Blueprint("visits", __name__)


@visits_bp.route("/visits", methods=["POST"])
@jwt_required()
def create_visit():

    data = request.json

    visit = Visit(
        user_id=get_jwt_identity(),
        property_id=data["property_id"],
        property_name=data["property_name"],
        city=data["city"],
        locality=data["locality"],
        visit_date=data["visit_date"]
    )

    db.session.add(visit)
    db.session.commit()

    return {"message": "visit booked"}


@visits_bp.route("/visits/my-visits")
@jwt_required()
def my_visits():

    user_id = get_jwt_identity()

    visits = Visit.query.filter_by(user_id=user_id).all()

    result = []

    for v in visits:
        result.append({
            "id": v.id,
            "property_name": v.property_name,
            "city": v.city,
            "locality": v.locality,
            "visit_date": v.visit_date
        })

    return result