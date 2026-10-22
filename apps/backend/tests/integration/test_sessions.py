from fastapi.testclient import TestClient

from tests.integration.conftest import fetchval


def test_anonymous_session_is_an_httponly_cookie_by_default(client: TestClient) -> None:
    response = client.post("/api/v1/sessions/anonymous")

    assert response.status_code == 201
    assert response.json() == {"tier": 0, "token": None}
    set_cookie = response.headers["set-cookie"].lower()
    assert "ap_session=" in set_cookie and "httponly" in set_cookie and "samesite=lax" in set_cookie
    assert client.get("/api/v1/sessions/me").json() == {"tier": 0, "token": None}


def test_native_clients_get_a_bearer_token_instead_of_a_cookie(client: TestClient) -> None:
    response = client.post("/api/v1/sessions/anonymous", json={"delivery": "token"})

    token = response.json()["token"]
    assert response.status_code == 201 and token
    assert "set-cookie" not in response.headers
    me = client.get("/api/v1/sessions/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200


def test_starting_again_on_the_same_device_reuses_the_session(
    client: TestClient, clean_db: str
) -> None:
    client.post("/api/v1/sessions/anonymous")
    again = client.post("/api/v1/sessions/anonymous")

    assert again.status_code == 200
    assert fetchval(clean_db, "SELECT count(*) FROM identity.actor") == 1


def test_only_the_token_hash_is_stored(client: TestClient, clean_db: str) -> None:
    token = client.post("/api/v1/sessions/anonymous", json={"delivery": "token"}).json()["token"]

    stored = fetchval(clean_db, "SELECT token_hash FROM identity.session")
    assert isinstance(stored, bytes) and token.encode() not in stored and len(stored) == 32


def test_me_without_a_session_is_401_with_a_machine_code(client: TestClient) -> None:
    response = client.get("/api/v1/sessions/me")

    assert response.status_code == 401
    assert response.json()["detail"]["code"] == "session_required"


def test_unknown_bearer_token_is_rejected(client: TestClient) -> None:
    response = client.get("/api/v1/sessions/me", headers={"Authorization": "Bearer nope"})

    assert response.status_code == 401
