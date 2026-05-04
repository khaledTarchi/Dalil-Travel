from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__)

# Catch-all route to serve the SPA
@views_bp.route('/', defaults={'path': ''})
@views_bp.route('/<path:path>')
def catch_all(path):
    # Only serve index.html for non-api routes
    if path.startswith('api/'):
        return "Not Found", 404
    return render_template('index.html')
