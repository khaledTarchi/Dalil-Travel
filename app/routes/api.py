from flask import Blueprint, jsonify, request
from ..db import get_db
from ..ai import get_ai_guide_info

api_bp = Blueprint('api', __name__)

@api_bp.route('/destinations', methods=['GET'])
def get_destinations():
    lang = request.args.get('lang', 'en')
    db = get_db()
    cursor = db.cursor()
    
    query = """
        SELECT d.id, d.lat, d.lng, d.image_url, 
               COALESCE(t_lang.name, t_en.name) as name, 
               COALESCE(t_lang.description, t_en.description) as description 
        FROM Destinations d
        LEFT JOIN Translations t_lang ON d.id = t_lang.entity_id AND t_lang.entity_type = 'destination' AND t_lang.language_code = ?
        LEFT JOIN Translations t_en ON d.id = t_en.entity_id AND t_en.entity_type = 'destination' AND t_en.language_code = 'en'
    """
    cursor.execute(query, (lang,))
    rows = cursor.fetchall()
    
    destinations = []
    for row in rows:
        destinations.append({
            'id': row['id'],
            'lat': row['lat'],
            'lng': row['lng'],
            'image_url': row['image_url'],
            'name': row['name'],
            'description': row['description']
        })
    return jsonify(destinations)

@api_bp.route('/destinations/<int:dest_id>', methods=['GET'])
def get_destination(dest_id):
    lang = request.args.get('lang', 'en')
    db = get_db()
    cursor = db.cursor()
    
    query = """
        SELECT d.id, d.lat, d.lng, d.image_url, 
               COALESCE(t_lang.name, t_en.name) as name, 
               COALESCE(t_lang.description, t_en.description) as description 
        FROM Destinations d
        LEFT JOIN Translations t_lang ON d.id = t_lang.entity_id AND t_lang.entity_type = 'destination' AND t_lang.language_code = ?
        LEFT JOIN Translations t_en ON d.id = t_en.entity_id AND t_en.entity_type = 'destination' AND t_en.language_code = 'en'
        WHERE d.id = ?
    """
    cursor.execute(query, (lang, dest_id))
    row = cursor.fetchone()
    
    if row:
        return jsonify({
            'id': row['id'],
            'lat': row['lat'],
            'lng': row['lng'],
            'image_url': row['image_url'],
            'name': row['name'],
            'description': row['description']
        })
    return jsonify({'error': 'Destination not found'}), 404

@api_bp.route('/services/<int:destination_id>', methods=['GET'])
def get_services(destination_id):
    lang = request.args.get('lang', 'en')
    db = get_db()
    cursor = db.cursor()
    
    query = """
        SELECT s.id, s.type, s.base_price, s.rating, s.is_sponsored, s.image_url,
               COALESCE(t_lang.name, t_en.name) as name, 
               COALESCE(t_lang.description, t_en.description) as description, 
               u.company_name
        FROM Services s
        LEFT JOIN Translations t_lang ON s.id = t_lang.entity_id AND t_lang.entity_type = 'service' AND t_lang.language_code = ?
        LEFT JOIN Translations t_en ON s.id = t_en.entity_id AND t_en.entity_type = 'service' AND t_en.language_code = 'en'
        LEFT JOIN Users u ON s.provider_id = u.id
        WHERE s.destination_id = ?
    """
    cursor.execute(query, (lang, destination_id))
    rows = cursor.fetchall()
    
    services = []
    for row in rows:
        services.append({
            'id': row['id'],
            'type': row['type'],
            'base_price': row['base_price'],
            'rating': row['rating'],
            'is_sponsored': bool(row['is_sponsored']),
            'image_url': row['image_url'],
            'name': row['name'],
            'description': row['description'],
            'company_name': row['company_name']
        })
    return jsonify(services)

@api_bp.route('/service/<int:service_id>', methods=['GET'])
def get_service(service_id):
    lang = request.args.get('lang', 'en')
    db = get_db()
    cursor = db.cursor()
    
    query = """
        SELECT s.id, s.destination_id, s.type, s.base_price, s.rating, s.is_sponsored, s.image_url,
               COALESCE(t_lang.name, t_en.name) as name, 
               COALESCE(t_lang.description, t_en.description) as description, 
               u.company_name
        FROM Services s
        LEFT JOIN Translations t_lang ON s.id = t_lang.entity_id AND t_lang.entity_type = 'service' AND t_lang.language_code = ?
        LEFT JOIN Translations t_en ON s.id = t_en.entity_id AND t_en.entity_type = 'service' AND t_en.language_code = 'en'
        LEFT JOIN Users u ON s.provider_id = u.id
        WHERE s.id = ?
    """
    cursor.execute(query, (lang, service_id))
    row = cursor.fetchone()
    
    if row:
        return jsonify({
            'id': row['id'],
            'destination_id': row['destination_id'],
            'type': row['type'],
            'base_price': row['base_price'],
            'rating': row['rating'],
            'is_sponsored': bool(row['is_sponsored']),
            'image_url': row['image_url'],
            'name': row['name'],
            'description': row['description'],
            'company_name': row['company_name']
        })
    return jsonify({'error': 'Service not found'}), 404

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password') # Plain text for prototype
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, first_name, last_name, email, role, preferred_language FROM Users WHERE email = ? AND password = ?", (email, password))
    row = cursor.fetchone()
    
    if row:
        return jsonify({
            'success': True,
            'user': {
                'id': row['id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'role': row['role'],
                'preferred_language': row['preferred_language']
            }
        })
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

@api_bp.route('/bookings', methods=['POST'])
def create_booking():
    data = request.json
    user_id = data.get('user_id')
    service_id = data.get('service_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    total_amount = data.get('total_amount')
    payment_method = data.get('payment_method')
    
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO Bookings (user_id, service_id, start_date, end_date, total_amount, payment_status) VALUES (?, ?, ?, ?, ?, 'pending')",
            (user_id, service_id, start_date, end_date, total_amount)
        )
        db.commit()
        return jsonify({'success': True, 'booking_id': cursor.lastrowid})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/bookings/<int:user_id>', methods=['GET'])
def get_user_bookings(user_id):
    lang = request.args.get('lang', 'en')
    db = get_db()
    cursor = db.cursor()
    
    query = """
        SELECT b.id, b.start_date, b.end_date, b.total_amount, b.payment_status, 
               s.id as service_id, s.type, s.destination_id,
               COALESCE(t_lang.name, t_en.name) as service_name, 
               COALESCE(dt_lang.name, dt_en.name) as destination_name, 
               d.image_url as destination_image
        FROM Bookings b
        JOIN Services s ON b.service_id = s.id
        LEFT JOIN Translations t_lang ON s.id = t_lang.entity_id AND t_lang.entity_type = 'service' AND t_lang.language_code = ?
        LEFT JOIN Translations t_en ON s.id = t_en.entity_id AND t_en.entity_type = 'service' AND t_en.language_code = 'en'
        JOIN Destinations d ON s.destination_id = d.id
        LEFT JOIN Translations dt_lang ON d.id = dt_lang.entity_id AND dt_lang.entity_type = 'destination' AND dt_lang.language_code = ?
        LEFT JOIN Translations dt_en ON d.id = dt_en.entity_id AND dt_en.entity_type = 'destination' AND dt_en.language_code = 'en'
        WHERE b.user_id = ?
    """
    cursor.execute(query, (lang, lang, user_id))
    rows = cursor.fetchall()
    
    bookings = []
    for row in rows:
        bookings.append({
            'id': row['id'],
            'start_date': row['start_date'],
            'end_date': row['end_date'],
            'total_amount': row['total_amount'],
            'payment_status': row['payment_status'],
            'service_id': row['service_id'],
            'service_type': row['type'],
            'service_name': row['service_name'],
            'destination_id': row['destination_id'],
            'destination_name': row['destination_name'],
            'destination_image': row['destination_image']
        })
    return jsonify(bookings)

@api_bp.route('/ai-guide', methods=['POST'])
def ai_guide():
    data = request.json
    location_name = data.get('location_name')
    user_language = data.get('user_language', 'English')
    
    if not location_name:
        return jsonify({'error': 'location_name is required'}), 400
        
    info = get_ai_guide_info(location_name, user_language)
    return jsonify({'info': info})

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO Users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)",
            (first_name, last_name, email, password)
        )
        db.commit()
        return jsonify({'success': True, 'user_id': cursor.lastrowid})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'Email already exists'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
