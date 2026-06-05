from flask import Flask, request, g
import os
from config import Config
from .extensions import db
from .utils.i18n import load_translations

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Load translations once at startup or per request based on preference
    # Since it's a simple JSON dictionary, we can load it into app.config or attach it
    translations = load_translations(os.path.join(app.root_path, 'translations'))
    app.config['TRANSLATIONS'] = translations
    
    # Disable caching for static files
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    
    # Context processor for global variables and translation
    @app.context_processor
    def inject_globals():
        lang = request.args.get('lang') or request.cookies.get('lang') or app.config['DEFAULT_LANGUAGE']
        if lang not in app.config['SUPPORTED_LANGUAGES']:
            lang = app.config['DEFAULT_LANGUAGE']
            
        def _t(key):
            # Simple translation function
            return app.config['TRANSLATIONS'].get(lang, {}).get(key, key)
            
        return {
            'SITE_NAME': app.config['SITE_NAME'],
            'CURRENCY': app.config['CURRENCY'],
            '_t': _t,
            'current_lang': lang
        }

    # Register blueprints
    from .routes.main import main_bp
    app.register_blueprint(main_bp)
    
    # Removed api.py registration as it is obsolete

    @app.after_request
    def add_header(response):
        # Disable caching for all responses
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

    return app
