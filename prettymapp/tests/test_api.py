import os
import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from api import app

load_dotenv()

client = TestClient(app)
API_KEY = os.getenv("API_KEY")

def test_generate_map_with_valid_api_key():
    response = client.post(
        "/",
        json={"location": "Berlin", "radius": 1000, "style": "Peach"},
        headers={"X-API-Key": API_KEY},
    )
    assert response.status_code == 200
    assert "image_url" in response.json()

def test_generate_map_with_invalid_api_key():
    response = client.post(
        "/",
        json={"location": "Berlin", "radius": 1000, "style": "Peach"},
        headers={"X-API-Key": "invalid_api_key"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid API Key"}

def test_generate_map_without_api_key():
    response = client.post(
        "/",
        json={"location": "Berlin", "radius": 1000, "style": "Peach"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid API Key"}
