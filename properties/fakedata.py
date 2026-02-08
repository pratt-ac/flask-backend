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
    "https://picsum.photos/400/300?random=1",
    "https://picsum.photos/400/300?random=2",
    "https://picsum.photos/400/300?random=3",
    "https://picsum.photos/400/300?random=4",
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
