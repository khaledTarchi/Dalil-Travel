import json
import os

def load_translations(translations_dir):
    """
    Loads JSON translation files from the translations directory.
    Returns a dictionary structured as:
    {
        'en': {'Welcome': 'Welcome', ...},
        'fr': {'Welcome': 'Bienvenue', ...},
        'ar': {'Welcome': 'مرحباً', ...}
    }
    """
    translations = {}
    if not os.path.exists(translations_dir):
        return translations
        
    for filename in os.listdir(translations_dir):
        if filename.endswith('.json'):
            lang_code = filename.split('.')[0]
            with open(os.path.join(translations_dir, filename), 'r', encoding='utf-8') as f:
                try:
                    translations[lang_code] = json.load(f)
                except json.JSONDecodeError:
                    print(f"Error loading translation file {filename}")
                    translations[lang_code] = {}
                    
    return translations
