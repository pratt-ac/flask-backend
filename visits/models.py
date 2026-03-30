

from db import db
from datetime import datetime

class Visit(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, nullable=False)
    property_id = db.Column(db.Integer, nullable=False)

    property_name = db.Column(db.String(200))
    city = db.Column(db.String(100))
    locality = db.Column(db.String(100))

    visit_date = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)