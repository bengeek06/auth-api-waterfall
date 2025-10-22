"""
Configuration resource for the Flask API.

This module provides an endpoint to retrieve current application
configuration information for debugging and monitoring purposes.
"""

import os
from flask_restful import Resource


class ConfigResource(Resource):
    """
    Resource for providing the application configuration.

    Methods:
        get():
            Retrieve the current application configuration.
    """

    def get(self):
        """
        Retrieve the current application configuration.

        Returns:
            dict: A dictionary containing the application configuration and
            HTTP status code 200.
        """
        config = {
            "FLASK_ENV": os.getenv("FLASK_ENV"),
            "DATABASE_URL": os.getenv("DATABASE_URL"),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
            "USER_SERVICE_URL": os.getenv("USER_SERVICE_URL"),
        }
        return config, 200
