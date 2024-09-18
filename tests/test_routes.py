import pytest
import os
import sys

# Add the parent directory to the path so that we can import the app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_history_page(client):
    response = client.get('/history')
    assert response.status_code == 200

def test_non_existent_page(client):
    response = client.get('/non-existent')
    assert response.status_code == 404