from flask import Flask
from .routes.api import api_bp
from .routes.views import views_bp
import os

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    
    # Disable caching for static files
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(views_bp)

    @app.after_request
    def add_header(response):
        # Disable caching for all responses
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return app
