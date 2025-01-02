import pytest
import json
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health-check')
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}

def test_add_text(client):
    response = client.post('/add_text',
                           data=json.dumps({"text": "Test text"}),
                           content_type='application/json')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["status"] == "success"
    assert "id" in response_data

def test_add_text_no_text(client):
    response = client.post('/add_text',
                           data=json.dumps({}),
                           content_type='application/json')
    assert response.status_code == 400
    response_data = response.get_json()
    assert response_data["error"] == "No text provided"

def test_find_similar(client):
    # Add a text first
    client.post('/add_text',
                data=json.dumps({"text": "Test text"}),
                content_type='application/json')

    response = client.post('/find_similar',
                           data=json.dumps({"text": "Test text", "n": 1}),
                           content_type='application/json')
    assert response.status_code == 200
    response_data = response.get_json()
    assert "results" in response_data
    assert len(response_data["results"]) > 0

def test_find_similar_no_text(client):
    response = client.post('/find_similar',
                           data=json.dumps({}),
                           content_type='application/json')
    assert response.status_code == 400
    response_data = response.get_json()
    assert response_data["error"] == "No text provided"

def test_find_similar_no_data(client):
    response = client.post('/find_similar', content_type='application/json')
    assert response.status_code == 400
    response_data = response.get_json()
    assert response_data["error"] == "No text provided"
