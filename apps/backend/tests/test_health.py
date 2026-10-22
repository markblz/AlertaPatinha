from fastapi.testclient import TestClient

from api.main import app


def test_liveness_does_not_touch_the_database() -> None:
    response = TestClient(app).get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
