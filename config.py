import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_for_mvp'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'dalil.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Global Config Variables
    SITE_NAME = 'Dhiafa dz'
    CURRENCY = 'DZD'
    SUPPORTED_LANGUAGES = ['en', 'fr', 'ar']
    DEFAULT_LANGUAGE = 'fr'
