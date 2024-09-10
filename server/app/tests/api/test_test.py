from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_test():
    response = client.get("/api/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from Picasso"}
