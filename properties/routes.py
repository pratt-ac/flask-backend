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

@properties_bp.route("/<int:id>", methods=["GET"])
def get_property(id):
    """
    Full property details endpoint.
    Used for property detail page.
    """

    p = Property.query.get_or_404(id)

    return jsonify({
        "id": p.id,
        "name": p.name,
        "bhk": p.bhk,
        "price": p.price,
        "sqft": p.sqft,
        "city": p.city,
        "locality": p.locality,
        "thumbnail": p.thumbnail_url,
        "lat": p.latitude,
        "lng": p.longitude,
        "description": p.description
    })


@properties_bp.route("/fair-price/<int:property_id>")
def fair_price(property_id):

    prop = Property.query.get_or_404(property_id)

    # Define similarity range
    min_sqft = prop.sqft * 0.8
    max_sqft = prop.sqft * 1.2

    # Find comparable properties
    comps = Property.query.filter(
        Property.city == prop.city,
        Property.bhk == prop.bhk,
        Property.sqft >= min_sqft,
        Property.sqft <= max_sqft,
        Property.id != prop.id
    ).all()

    if len(comps) == 0:
        return {"message": "Not enough comparable properties"}

    # Calculate average price per sqft
    price_per_sqft = [c.price / c.sqft for c in comps]
    avg_price_per_sqft = sum(price_per_sqft) / len(price_per_sqft)

    # Expected fair price
    expected_price = avg_price_per_sqft * prop.sqft

    diff_percent = ((prop.price - expected_price) / expected_price) * 100

    if diff_percent < -10:
        verdict = "Underpriced"
    elif diff_percent > 10:
        verdict = "Overpriced"
    else:
        verdict = "Fair Price"

    return {
        "city": prop.city,
        "bhk": prop.bhk,
        "sqft": prop.sqft,
        "comparable_properties": len(comps),
        "expected_price": round(expected_price),
        "actual_price": prop.price,
        "difference_percent": round(diff_percent, 2),
        "verdict": verdict
    }