"""Pytest configuration and fixtures"""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def test_client():
    """Fixture to provide a test client for API testing"""
    from backend.main import app
    return TestClient(app)
