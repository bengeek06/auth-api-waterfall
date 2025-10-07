"""
Route registration module.

This module handles the registration of all API routes for the Flask application.
It imports and registers blueprints or route handlers from various modules.
"""

from flask_restful import Api

from app.logger import logger
from app.resources.version import VersionResource
from app.resources.config import ConfigResource
from app.resources.login import LoginResource
from app.resources.logout import LogoutResource
from app.resources.verify import VerifyResource
from app.resources.refresh import RefreshResource
from app.resources.health import HealthResource




def register_routes(app):
    """
    Register the REST API routes on the Flask application.

    Args:
        app (Flask): The Flask application instance.

    This function creates a Flask-RESTful Api instance, adds the resource
    endpoints for managing dummy items, and logs the successful registration
    of routes.
    """
    api = Api(app)

    api.add_resource(VersionResource, "/version")
    api.add_resource(ConfigResource, "/config")
    api.add_resource(LoginResource, "/login")
    api.add_resource(LogoutResource, "/logout")
    api.add_resource(VerifyResource, "/verify")
    api.add_resource(RefreshResource, "/refresh")
    api.add_resource(HealthResource, "/health")

    logger.info("Routes registered successfully (including /docs & /redoc).")
