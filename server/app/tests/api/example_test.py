from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_example_get():
    response = client.get("/api/example")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello from Picasso",
        "context": "This is an example GET endpoint.",
    }
