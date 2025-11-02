"""Pytest fixtures for backend tests."""
import pytest
from app.database.init_database import init_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Initialize the database schema before running tests."""
    init_db()
    yield
