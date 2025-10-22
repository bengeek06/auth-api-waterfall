"""
Database models initialization module.

This module initializes the SQLAlchemy database instance and imports
all model classes to ensure they are registered with SQLAlchemy.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
