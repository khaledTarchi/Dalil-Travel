import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "dalil.db")

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed existing database at {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Tables
    cursor.executescript("""
        CREATE TABLE Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            preferred_language TEXT DEFAULT 'en',
            is_agency BOOLEAN DEFAULT 0,
            company_name TEXT NULL
        );

        CREATE TABLE Destinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            image_url TEXT NOT NULL
        );

        CREATE TABLE Translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_type TEXT NOT NULL, -- 'destination', 'service'
            entity_id INTEGER NOT NULL,
            language_code TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT
        );

        CREATE TABLE Services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination_id INTEGER NOT NULL,
            type TEXT NOT NULL, -- 'accommodation', 'transport', 'guide', 'food', 'insurance'
            base_price REAL NOT NULL,
            rating REAL DEFAULT 0,
            is_sponsored BOOLEAN DEFAULT 0,
            provider_id INTEGER,
            image_url TEXT NOT NULL,
            FOREIGN KEY(destination_id) REFERENCES Destinations(id),
            FOREIGN KEY(provider_id) REFERENCES Users(id)
        );

        CREATE TABLE Bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            payment_status TEXT DEFAULT 'pending',
            FOREIGN KEY(user_id) REFERENCES Users(id),
            FOREIGN KEY(service_id) REFERENCES Services(id)
        );
    """)

    # Insert Mock Data
    
    # Users
    cursor.execute("INSERT INTO Users (first_name, last_name, email, password, role) VALUES ('Admin', 'User', 'admin@dalil.dz', 'password123', 'admin')")
    cursor.execute("INSERT INTO Users (first_name, last_name, email, password, role) VALUES ('Test', 'User', 'test@example.com', 'test', 'user')")
    cursor.execute("INSERT INTO Users (first_name, last_name, email, password, role, is_agency, company_name) VALUES ('Dzair', 'Rent', 'contact@dzairrent.dz', 'password123', 'partner', 1, 'Dzair Rent Car')")
    cursor.execute("INSERT INTO Users (first_name, last_name, email, password, role, is_agency, company_name) VALUES ('El-Djazair', 'Hotel', 'contact@eldjazair.dz', 'password123', 'partner', 1, 'Hotel El-Djazair')")

    # Destinations
    destinations = [
        (35.6987, -0.6308, "/static/img/oran.png"), # 1 Oran
        (28.0339, 1.6596, "/static/img/sahara.png"), # 2 Sahara
        (34.8783, -1.3150, "/static/img/tlemcen.png"), # 3 Tlemcen
        (36.3650, 6.6147, "/static/img/constantine.png"), # 4 Constantine
        (36.7538, 3.0588, "/static/img/algiers.png"), # 5 Algiers
        (36.7558, 5.0843, "/static/img/bejaia.png"), # 6 Bejaia
        (36.8206, 5.7667, "/static/img/jijel.png"), # 7 Jijel
        (32.4909, 3.6735, "/static/img/ghardaia.png") # 8 Ghardaia
    ]
    cursor.executemany("INSERT INTO Destinations (lat, lng, image_url) VALUES (?, ?, ?)", destinations)

    # Translations for Destinations
    translations = [
        # Oran
        ('destination', 1, 'en', 'Oran', 'The radiant city overlooking the Mediterranean.'),
        ('destination', 1, 'fr', 'Oran', 'La ville radieuse surplombant la Méditerranée.'),
        ('destination', 1, 'ar', 'وهران', 'المدينة الباهية المطلة على البحر الأبيض المتوسط.'),
        # Sahara
        ('destination', 2, 'en', 'Sahara Desert', 'A vast, breathtaking expanse of golden dunes.'),
        ('destination', 2, 'fr', 'Désert du Sahara', 'Une vaste et époustouflante étendue de dunes dorées.'),
        ('destination', 2, 'ar', 'الصحراء الكبرى', 'امتداد شاسع ومذهل من الكثبان الذهبية.'),
        # Tlemcen
        ('destination', 3, 'en', 'Tlemcen', 'The pearl of the Maghreb, known for Moorish buildings.'),
        ('destination', 3, 'fr', 'Tlemcen', 'La perle du Maghreb, connue pour ses bâtiments mauresques.'),
        ('destination', 3, 'ar', 'تلمسان', 'لؤلؤة المغرب العربي، تشتهر بمبانيها المغاربية.'),
        # Constantine
        ('destination', 4, 'en', 'Constantine', 'The city of bridges, built on a dramatic ravine.'),
        ('destination', 4, 'fr', 'Constantine', 'La ville des ponts, construite sur un ravin spectaculaire.'),
        ('destination', 4, 'ar', 'قسنطينة', 'مدينة الجسور، مبنية على وادٍ درامي.'),
        # Algiers
        ('destination', 5, 'en', 'Algiers', 'The white city on the bay.'),
        ('destination', 5, 'fr', 'Alger', 'La ville blanche sur la baie.'),
        ('destination', 5, 'ar', 'الجزائر', 'المدينة البيضاء على الخليج.'),
        # Bejaia
        ('destination', 6, 'en', 'Bejaia', 'Coastal beauty and ancient history.'),
        ('destination', 6, 'fr', 'Béjaïa', 'Beauté côtière et histoire ancienne.'),
        ('destination', 6, 'ar', 'بجاية', 'الجمال الساحلي والتاريخ القديم.'),
        # Jijel
        ('destination', 7, 'en', 'Jijel', 'Stunning corniche and caves.'),
        ('destination', 7, 'fr', 'Jijel', 'Corniche et grottes magnifiques.'),
        ('destination', 7, 'ar', 'جيجل', 'كورنيش وكهوف مذهلة.'),
        # Ghardaia
        ('destination', 8, 'en', 'Ghardaia', 'The pearl of the Mzab valley.'),
        ('destination', 8, 'fr', 'Ghardaïa', 'La perle de la vallée du Mzab.'),
        ('destination', 8, 'ar', 'غرداية', 'لؤلؤة وادي ميزاب.')
    ]
    cursor.executemany("INSERT INTO Translations (entity_type, entity_id, language_code, name, description) VALUES (?, ?, ?, ?, ?)", translations)

    # Services
    services = [
        # Oran (1)
        (1, 'accommodation', 15000.0, 4.8, 0, 4, '/static/img/luxury_hotel.png'), # 1
        (1, 'accommodation', 8000.0, 4.2, 0, None, '/static/img/traditional_hotel.png'), # 2
        (1, 'food', 3000.0, 4.5, 0, None, '/static/img/seafood_restaurant.png'), # 3
        (1, 'transport', 4500.0, 4.4, 0, 3, '/static/img/vip_transport.png'), # 4
        
        # Sahara (2)
        (2, 'guide', 8000.0, 4.9, 0, None, '/static/img/desert_guide.png'), # 5
        (2, 'transport', 12000.0, 4.6, 1, 3, '/static/img/vip_transport.png'), # 6
        (2, 'accommodation', 5000.0, 4.1, 0, None, '/static/img/traditional_hotel.png'), # 7
        
        # Tlemcen (3)
        (3, 'accommodation', 10000.0, 4.7, 0, None, '/static/img/luxury_hotel.png'), # 8
        (3, 'food', 2500.0, 4.6, 0, None, '/static/img/traditional_restaurant.png'), # 9
        (3, 'guide', 3500.0, 4.8, 0, None, '/static/img/tour_guide.png'), # 10
        
        # Constantine (4)
        (4, 'food', 2500.0, 4.4, 0, None, '/static/img/traditional_restaurant.png'), # 11
        (4, 'accommodation', 12000.0, 4.5, 0, None, '/static/img/luxury_hotel.png'), # 12
        (4, 'guide', 4000.0, 4.7, 0, None, '/static/img/tour_guide.png'), # 13
        
        # Algiers (5)
        (5, 'accommodation', 20000.0, 4.9, 1, 4, '/static/img/luxury_hotel.png'), # 14
        (5, 'accommodation', 18000.0, 4.8, 0, None, '/static/img/traditional_hotel.png'), # 15
        (5, 'food', 4000.0, 4.7, 0, None, '/static/img/traditional_restaurant.png'), # 16
        (5, 'transport', 3500.0, 4.5, 0, 3, '/static/img/vip_transport.png'), # 17
        
        # Bejaia (6)
        (6, 'accommodation', 12000.0, 4.6, 0, None, '/static/img/traditional_hotel.png'), # 18
        (6, 'guide', 3000.0, 4.9, 0, None, '/static/img/tour_guide.png'), # 19
        (6, 'food', 2000.0, 4.3, 0, None, '/static/img/seafood_restaurant.png'), # 20
        
        # Jijel (7)
        (7, 'transport', 5000.0, 4.3, 0, 3, '/static/img/coastal_transport.png'), # 21
        (7, 'accommodation', 9000.0, 4.4, 0, None, '/static/img/traditional_hotel.png'), # 22
        (7, 'guide', 2500.0, 4.6, 0, None, '/static/img/tour_guide.png'), # 23
        
        # Ghardaia (8)
        (8, 'guide', 6000.0, 4.8, 0, None, '/static/img/desert_guide.png'), # 24
        (8, 'accommodation', 7500.0, 4.7, 0, None, '/static/img/traditional_hotel.png'), # 25
        (8, 'food', 1800.0, 4.5, 0, None, '/static/img/traditional_restaurant.png') # 26
    ]
    cursor.executemany("INSERT INTO Services (destination_id, type, base_price, rating, is_sponsored, provider_id, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)", services)

    # Service Translations
    service_translations = [
        ('service', 1, 'en', 'Royal Hotel Oran', 'Luxury stay with sea view.'),
        ('service', 2, 'en', 'Eden Phoenix Hotel', 'Comfortable business hotel near airport.'),
        ('service', 3, 'en', 'Le Corsaire', 'Seafood restaurant at the port.'),
        ('service', 4, 'en', 'Oran Airport Transfer', 'Private ride from ORN airport.'),
        
        ('service', 5, 'en', 'Tuareg Expedition Guide', 'Experienced local desert guide.'),
        ('service', 6, 'en', 'Desert 4x4 Safari', 'Thrilling ride across the dunes.'),
        ('service', 7, 'en', 'Oasis Camp', 'Traditional tent sleeping under stars.'),
        
        ('service', 8, 'en', 'Renaissance Tlemcen', 'Elegant hotel near the plateau.'),
        ('service', 9, 'en', 'Lalla Setti Restaurant', 'Dine with a view over Tlemcen.'),
        ('service', 10, 'en', 'Moorish History Tour', 'Walking tour of Islamic ruins.'),
        
        ('service', 11, 'en', 'Cirta Cuisine', 'Traditional Algerian food.'),
        ('service', 12, 'en', 'Marriott Constantine', '5-star comfort downtown.'),
        ('service', 13, 'en', 'Bridges Tour', 'Guided walk across the 7 bridges.'),
        
        ('service', 14, 'en', 'Hotel El-Djazair Algiers', 'Historic and luxurious.'),
        ('service', 15, 'en', 'Sofitel Algiers', 'Premium high-rise hotel.'),
        ('service', 16, 'en', 'Casbah Traditional Dining', 'Authentic flavors in old town.'),
        ('service', 17, 'en', 'VIP City Transfer', 'Luxury car around the capital.'),
        
        ('service', 18, 'en', 'Bejaia Beach Resort', 'Relaxing stay by the beach.'),
        ('service', 19, 'en', 'Yemma Gouraya Hike', 'Guided trek to the peak.'),
        ('service', 20, 'en', 'Cap Carbon Cafe', 'Coffee with monkey views.'),
        
        ('service', 21, 'en', 'Jijel Coastal Transport', 'Reliable transport around the corniche.'),
        ('service', 22, 'en', 'Corniche Hotel', 'Family friendly stay.'),
        ('service', 23, 'en', 'Marvelous Caves Tour', 'Boat ride into the sea caves.'),
        
        ('service', 24, 'en', 'Mzab Valley Tour', 'Explore the unique architecture of Ghardaia.'),
        ('service', 25, 'en', 'Traditional Guest House', 'Authentic adobe home experience.'),
        ('service', 26, 'en', 'Oasis Date Cafe', 'Fresh dates and mint tea.')
    ]
    cursor.executemany("INSERT INTO Translations (entity_type, entity_id, language_code, name, description) VALUES (?, ?, ?, ?, ?)", service_translations)

    # Bookings
    bookings = [
        (2, 1, '2026-06-01', '2026-06-05', 60000.0, 'paid'),
        (2, 3, '2026-07-10', '2026-07-12', 16000.0, 'pending')
    ]
    cursor.executemany("INSERT INTO Bookings (user_id, service_id, start_date, end_date, total_amount, payment_status) VALUES (?, ?, ?, ?, ?, ?)", bookings)

    conn.commit()
    conn.close()
    print("Database initialized with mockup data.")

if __name__ == "__main__":
    init_db()
