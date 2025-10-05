"""
wsgi.py
-------
WSGI entry point for production deployment with Gunicorn.
"""

import os
from app import create_app

# Force production environment
os.environ['FLASK_ENV'] = 'production'

# Create application instance
app = create_app('app.config.ProductionConfig')

if __name__ == "__main__":
    app.run()