"""
Version resource for the Flask API.

This module provides an endpoint to retrieve the current application version information.
"""

from flask_restful import Resource

API_VERSION = "0.0.1"


class VersionResource(Resource):
    """
    Resource for providing the API version.

    Methods:
        get():
            Retrieve the current API version.
    """

    def get(self):
        """
        Retrieve the current API version.

        Returns:
            dict: A dictionary containing the API version and HTTP status
            code 200.
        """
        return {"version": API_VERSION}, 200
