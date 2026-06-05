from .extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user') # 'user', 'host', 'admin'
    preferred_language = db.Column(db.String(10), default='en')

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    region = db.Column(db.String(100), nullable=False) # e.g., 'Brezina', 'Timimoun'
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    price_per_night = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    
    # Connectivity & Utilities Index
    has_internet = db.Column(db.Boolean, default=False)
    internet_quality = db.Column(db.String(50), nullable=True) # e.g., '3G/4G Weak', 'Fiber'
    power_source = db.Column(db.String(100), nullable=True) # e.g., 'Solar Panels', 'Grid', 'Generator'
    capacity = db.Column(db.Integer, default=2)
    
    status = db.Column(db.String(50), default='active') # 'active', 'pending'

    host = db.relationship('User', backref=db.backref('properties', lazy=True))

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    
    property = db.relationship('Property', backref=db.backref('meals', lazy=True))

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    property = db.relationship('Property', backref=db.backref('bookings', lazy=True))

class RegistrationRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    image_urls = db.Column(db.Text, nullable=False) # comma-separated
    capacity = db.Column(db.Integer, nullable=False)
    has_internet = db.Column(db.Boolean, default=False)
    power_source = db.Column(db.String(100), nullable=False)
    meals_offered = db.Column(db.Text, nullable=True) # JSON or simple text description
    story = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='pending') # 'pending', 'approved', 'rejected'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
