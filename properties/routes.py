from flask import Blueprint, request, jsonify
from .models import Property

properties_bp = Blueprint("properties", __name__, url_prefix="/api/properties")


@properties_bp.route("", methods=["GET"])
def list_properties():
    """
    Card-level listing endpoint.
    Returns minimal data needed for property cards.
    """

    city = request.args.get("city")

    query = Property.query
    if city:
        query = query.filter_by(city=city)

    properties = query.all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "bhk": p.bhk,
            "price": p.price,
            "sqft": p.sqft,
            "city": p.city,
            "locality": p.locality,
            "thumbnail": p.thumbnail_url,
            "lat": p.latitude,
            "lng": p.longitude
        }
        for p in properties
    ])
