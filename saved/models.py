from db import db

class SavedProperty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "property_id", name="unique_user_property"),
    )
