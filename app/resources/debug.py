"""
Debug resource for development environment only.

This module provides debug endpoints that should NEVER be enabled in production.
"""

import os
from flask import request
from flask_restful import Resource
from app.logger import logger


class DebugTokensResource(Resource):
    """
    Debug resource to view current token values.

    **WARNING: This endpoint is only available in development/testing modes.**
    """

    def get(self):
        """
        Get current token values from cookies.

        Returns:
            dict: Current access and refresh tokens if available.
        """
        # Vérification de sécurité : seulement en développement
        if os.environ.get("FLASK_ENV") not in ("development", "testing"):
            logger.warning(
                "Debug endpoint accessed in non-development environment"
            )
            return {
                "message": "Endpoint not available in this environment"
            }, 404

        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        return {
            "access_token": access_token if access_token else None,
            "refresh_token": refresh_token if refresh_token else None,
            "note": "This endpoint is for development purposes only",
        }, 200
