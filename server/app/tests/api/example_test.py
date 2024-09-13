from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_example_get():
    response = client.get("/api/example")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Hello from Picasso",
        "context": "This is an example GET endpoint.",
    }
