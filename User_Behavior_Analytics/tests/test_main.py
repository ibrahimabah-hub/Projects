from fastapi.testclient import TestClient

from app.main import app
from database.database import _add_tables

_add_tables()
client = TestClient(app)

def test_greeting():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_create_visitor():
    response = client.post("/visitors/", json={"ip_address" : "0.0.3",
    "visits": [{
        "hits": [
        {
            "timestamp": "2026-09-09T12:00:00Z",
            "page_url": "/home"
        },
        {
            "timestamp": "2026-09-09T12:05:00Z",
            "page_url": "/about"
        }
    ]}]})
    assert response.status_code == 200

def test_read_visitors():
    response = client.get("/visitors/")
    assert response.status_code == 200

def test_read_visitor():
    response = client.get("/visitors/1")
    assert response.status_code == 200


def test_read_visits():
    response = client.get("/visits/")
    assert response.status_code == 200

def test_read_visit():
    response = client.get("/visits/1")
    assert response.status_code == 200