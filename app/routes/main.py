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
        title = request.form.get('title')
        region = request.form.get('region')
        price_per_night = request.form.get('price_per_night')
        capacity = request.form.get('capacity')
        has_internet = True if request.form.get('has_internet') == 'on' else False
        power_source = request.form.get('power_source')
        meals_offered = request.form.get('meals_offered')
        story = request.form.get('story')
        
        # Handle file upload
        image_url = ''
        if 'images' in request.files:
            file = request.files['images']
            if file and file.filename != '':
                import os
                import uuid
                from werkzeug.utils import secure_filename
                from flask import current_app
                
                base_filename = secure_filename(file.filename)
                if not base_filename:
                    base_filename = "upload.jpg"
                filename = f"{uuid.uuid4().hex}_{base_filename}"
                
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                image_url = f'/static/uploads/{filename}'
        
        # Get or create a host to assign this property to
        from ..models import User
        host = User.query.filter_by(role='host').first()
        if not host:
            safe_name = full_name if full_name else 'Host'
            safe_phone = phone if phone else '000000000'
            host = User(first_name=safe_name, last_name='(Host)', email=f'{safe_phone}@host.dz', password='password', role='host')
            db.session.add(host)
            db.session.commit()
            
        # Create the active Property directly so it appears on the map
        new_property = Property(
            host_id=host.id,
            title=title or 'Guesthouse',
            description=story or f"Welcome to our beautiful guesthouse in {region}.",
            region=region,
            price_per_night=float(price_per_night) if price_per_night else 0.0,
            image_url=image_url,
            has_internet=has_internet,
            power_source=power_source,
            capacity=int(capacity) if capacity else 2,
            status='active'
        )
        db.session.add(new_property)
        
        # Also store the original RegistrationRequest for record keeping
        request_obj = RegistrationRequest(
            full_name=full_name if full_name else 'Unknown',
            phone=phone if phone else 'Unknown',
            address=address if address else 'Unknown',
            image_urls=image_url,
            capacity=int(capacity) if capacity else 2,
            has_internet=has_internet,
            power_source=power_source,
            meals_offered=meals_offered,
            story=story,
            status='approved'
        )
        db.session.add(request_obj)
        db.session.commit()
        
        # Flash message and redirect
        flash("Property successfully registered and is now live!", "success")
        return redirect(url_for('main.explore', region=region))

    return render_template('register_property.html')

@main_bp.route('/about')
def about():
    # About the Project & Innovation
    return render_template('about.html')
