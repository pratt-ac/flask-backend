import random
from .models import Property
from db import db


CITIES = {
    "Bangalore": ["Whitefield", "Indiranagar", "BTM", "Yelahanka"],
    "Mumbai": ["Andheri", "Powai", "Bandra", "Borivali"],
    "Delhi": ["Dwarka", "Saket", "Rohini", "Karol Bagh"],
    "Chennai": ["Velachery", "OMR", "Anna Nagar", "Tambaram"],
    "Hyderabad": ["Gachibowli", "Hitech City", "Kondapur", "Madhapur"]
}



THUMBNAILS = [
"https://images.unsplash.com/photo-1560185127-6ed189bf02f4?w=800&q=80",
"https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80",
"https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80",
"https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&q=80",
"https://images.unsplash.com/photo-1572120360610-d971b9d7767c?w=800&q=80",
"https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=800&q=80",
"https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800&q=80",
"https://images.unsplash.com/photo-1600210492493-0946911123ea?w=800&q=80"
]

def seed_properties(count_per_city=50):
    # Prevent reseeding on every restart
    if Property.query.first():
        return

    for city, localities in CITIES.items():
        for _ in range(count_per_city):
            locality = random.choice(localities)

            prop = Property(
                name=f"{random.choice(['Sunrise', 'Greenview', 'Lakeview', 'Skyline'])} Residency",
                bhk=random.choice([1, 2, 3]),
                price=random.randint(50, 150) * 100000,
                sqft=random.randint(600, 2000),
                city=city,
                locality=locality,
                latitude=12.9 + random.random(),
                longitude=77.5 + random.random(),
                thumbnail_url=random.choice(THUMBNAILS),
                description="Spacious apartment in a prime residential area."
            )

            db.session.add(prop)

    db.session.commit()
