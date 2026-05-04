import sqlite3
import os
from flask import g

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dalil.db")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row # To access columns by name
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
