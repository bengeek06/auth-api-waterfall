"""
Tests for the version resource.

This module contains tests for the VersionResource API endpoint.
"""

import json


def test_version_endpoint(client):
    """
    Test the version endpoint returns expected response.

    This test verifies that the version endpoint returns the correct
    version information and HTTP status code.
    """

    response = client.get("/version")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert "version" in data
