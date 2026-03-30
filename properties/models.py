from db import db

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Basic info
    name = db.Column(db.String(100), nullable=False)
    bhk = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    sqft = db.Column(db.Integer, nullable=False)

    # Location
    city = db.Column(db.String(50), nullable=False)
    locality = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # Media & description
    thumbnail_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Metadata
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "bhk": self.bhk,
            "price": self.price,
            "sqft": self.sqft,
            "city": self.city,
            "locality": self.locality,
            "lat": self.latitude,
            "lng": self.longitude,
            "thumbnail": self.thumbnail_url,
            "description": self.description,
        }
    