"""
Health check resource for the Flask API.

This module provides an endpoint to check the health status of the
application and its dependencies.
"""

from flask_restful import Resource
from app.logger import logger


class HealthResource(Resource):
    """
    Resource for health check endpoint.

    This resource provides a simple way to check if the service is running
    and responding to requests.
    """

    def get(self):
        """
        Retrieve the health status of the application.

        Returns:
            dict: A dictionary containing the health status and
            HTTP status code 200.
        """
        logger.debug("Health check requested")

        return {
            "status": "healthy",
            "service": "auth_service",
            "message": "Service is running",
        }, 200
