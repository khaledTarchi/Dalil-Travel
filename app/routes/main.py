from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from ..models import Property, Meal, RegistrationRequest
from ..extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Home Page
    return render_template('index.html')

@main_bp.route('/set_lang')
def set_lang():
    lang = request.args.get('lang', 'fr')
    referrer = request.referrer or url_for('main.index')
    resp = make_response(redirect(referrer))
    resp.set_cookie('lang', lang, max_age=60*60*24*365) # 1 year
    return resp

@main_bp.route('/explore')
def explore():
    # Explore Accommodations
    region = request.args.get('region')
    if region:
        properties = Property.query.filter_by(region=region, status='active').all()
    else:
        properties = Property.query.filter_by(status='active').all()
    return render_template('explore.html', properties=properties, region=region)

@main_bp.route('/property/<int:id>')
def property_details(id):
    # Property Details & Booking
    property_obj = Property.query.get_or_404(id)
    return render_template('property.html', property=property_obj)

@main_bp.route('/register-property', methods=['GET', 'POST'])
def register_property():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        image_urls = request.form.get('image_urls')
        capacity = request.form.get('capacity')
        has_internet = True if request.form.get('has_internet') == 'on' else False
        power_source = request.form.get('power_source')
        meals_offered = request.form.get('meals_offered')
        story = request.form.get('story')
        
        request_obj = RegistrationRequest(
            full_name=full_name,
            phone=phone,
            address=address,
            image_urls=image_urls,
            capacity=capacity,
            has_internet=has_internet,
            power_source=power_source,
            meals_offered=meals_offered,
            story=story
        )
        db.session.add(request_obj)
        db.session.commit()
        
        # In a real app we might redirect to a success page or flash a message
        return render_template('register_success.html')

    return render_template('register_property.html')

@main_bp.route('/about')
def about():
    # About the Project & Innovation
    return render_template('about.html')
