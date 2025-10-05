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
import os
from flask import send_from_directory, make_response


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

    # -------- OpenAPI & Docs --------
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    @app.route("/openapi.yaml", methods=["GET"])
    def openapi_spec():
        """Serve the raw OpenAPI YAML specification."""
        return send_from_directory(project_root, "openapi.yml", mimetype="text/yaml")

    @app.route("/docs", methods=["GET"])
    def swagger_ui():
        """Serve Swagger UI pointing to /openapi.yaml."""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>API Docs - Swagger UI</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
  <style>
    body { margin:0; }
    .topbar { display: none; }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = () => {
      SwaggerUIBundle({
        url: '/openapi.yaml',
        dom_id: '#swagger-ui',
        presets: [SwaggerUIBundle.presets.apis],
        layout: "BaseLayout"
      });
    };
  </script>
</body>
</html>"""
        resp = make_response(html)
        resp.headers["Cache-Control"] = "no-store"
        return resp

    @app.route("/redoc", methods=["GET"])
    def redoc_ui():
        """Serve ReDoc documentation."""
        html = """<!DOCTYPE html>
<html>
  <head>
    <title>API Docs - ReDoc</title>
    <meta charset="utf-8"/>
    <style>
      body { margin:0; padding:0; }
    </style>
  </head>
  <body>
    <redoc spec-url='/openapi.yaml'></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"></script>
  </body>
</html>"""
        resp = make_response(html)
        resp.headers["Cache-Control"] = "no-store"
        return resp

    logger.info("Routes registered successfully (including /docs & /redoc).")
