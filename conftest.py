import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(__file__))

from app.main import app as fastapi_app

@pytest.fixture
def app():
    return fastapi_app
