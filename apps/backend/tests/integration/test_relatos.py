"""Relato create / detail / map through HTTP. Exercises the 🧠 policy, so these
stay red until src/geo/domain/policy.py and src/observations/domain/seen.py exist."""

import uuid
from typing import Any

from fastapi.testclient import TestClient

from src.geo.domain import cells
from src.geo.domain.types import Point
from tests.integration.conftest import fetchval
from tests.integration.privacy import assert_no_finer_than_cell

SE = Point(lat=-23.550520, lng=-46.633308)  # Praça da Sé
BBOX_SE = "-46.65,-23.57,-46.61,-23.53"


def relato(**overrides: Any) -> dict[str, Any]:
    body: dict[str, Any] = {
        "client_id": str(uuid.uuid4()),
        "kind": "emergency",
        "species": "dog",
        "location": {"lat": SE.lat, "lng": SE.lng, "accuracy_m": 12, "source": "gps"},
        "seen_text": "agora há pouco",
        "attributes": {"size": "medium", "coat_colors": ["caramel"], "injured": True},
    }
    body.update(overrides)
    return body


def start(client: TestClient) -> TestClient:
    client.post("/api/v1/sessions/anonymous")
    return client


def test_reporting_requires_a_session(client: TestClient) -> None:
    response = client.post("/api/v1/relatos", json=relato())

    assert response.status_code == 401


def test_create_returns_id_and_short_share_path(client: TestClient) -> None:
    response = start(client).post("/api/v1/relatos", json=relato())

    assert response.status_code == 201
    body = response.json()
    assert body["share_path"] == f"/r/{body['id']}"


def test_retrying_the_same_client_id_returns_the_same_relato(
    client: TestClient, clean_db: str
) -> None:
    start(client)
    body = relato()

    first = client.post("/api/v1/relatos", json=body)
    retry = client.post("/api/v1/relatos", json=body)

    assert retry.status_code == 200
    assert retry.json()["id"] == first.json()["id"]
    assert fetchval(clean_db, "SELECT count(*) FROM observations.observation") == 1


def test_another_device_cannot_claim_someone_elses_client_id(
    client: TestClient, other_client: TestClient
) -> None:
    body = relato()
    start(client).post("/api/v1/relatos", json=body)

    response = start(other_client).post("/api/v1/relatos", json=body)

    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "client_id_conflict"


def test_stored_relato_is_masked_at_write_time(client: TestClient, clean_db: str) -> None:
    start(client).post("/api/v1/relatos", json=relato())

    mode = fetchval(clean_db, "SELECT display_mode FROM observations.observation")
    cell = fetchval(clean_db, "SELECT display_cell::text FROM observations.observation")
    assert mode == "approximate"
    assert cell == cells.cell_of(SE, 9)


def test_free_text_attributes_are_rejected(client: TestClient) -> None:
    body = relato(attributes={"notes": "liga 11 99999-0000"})

    assert start(client).post("/api/v1/relatos", json=body).status_code == 422


def test_points_outside_brazil_are_rejected(client: TestClient) -> None:
    body = relato(location={"lat": 48.85, "lng": 2.35, "source": "gps"})

    assert start(client).post("/api/v1/relatos", json=body).status_code == 422


# ── detail ───────────────────────────────────────────────────────────────────


def test_reporter_sees_exact_and_the_read_is_logged(client: TestClient, clean_db: str) -> None:
    rid = start(client).post("/api/v1/relatos", json=relato()).json()["id"]

    body = client.get(f"/api/v1/relatos/{rid}").json()

    assert body["is_mine"] is True
    assert body["location"]["mode"] == "exact"
    assert body["location"]["geometry"] == {"type": "Point", "coordinates": [SE.lng, SE.lat]}
    assert fetchval(clean_db, "SELECT count(*) FROM geo.location_access_log") == 1


def test_another_device_gets_the_cell_and_no_log_row(
    client: TestClient, other_client: TestClient, clean_db: str
) -> None:
    rid = start(client).post("/api/v1/relatos", json=relato()).json()["id"]

    body = start(other_client).get(f"/api/v1/relatos/{rid}").json()

    assert body["is_mine"] is False and body["location"]["mode"] == "approximate"
    assert_no_finer_than_cell(body, SE, cells.cell_of(SE, 9))
    assert fetchval(clean_db, "SELECT count(*) FROM geo.location_access_log") == 0


def test_without_a_session_detail_is_public(client: TestClient, other_client: TestClient) -> None:
    rid = start(client).post("/api/v1/relatos", json=relato()).json()["id"]

    body = other_client.get(f"/api/v1/relatos/{rid}").json()

    assert_no_finer_than_cell(body, SE, cells.cell_of(SE, 9))


def test_public_time_is_coarsened(client: TestClient, other_client: TestClient) -> None:
    rid = start(client).post("/api/v1/relatos", json=relato()).json()["id"]

    seen = other_client.get(f"/api/v1/relatos/{rid}").json()["seen"]

    assert seen["precision"] == "hour"  # emergency → whole hours
    assert seen["start"].endswith(":00:00Z") or ":00:00" in seen["start"]


def test_unknown_relato_is_404(client: TestClient) -> None:
    response = client.get(f"/api/v1/relatos/{uuid.uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "relato_not_found"


# ── map ──────────────────────────────────────────────────────────────────────


def test_map_shows_the_hexagon_never_the_point(
    client: TestClient, other_client: TestClient
) -> None:
    start(client).post("/api/v1/relatos", json=relato())

    body = other_client.get("/api/v1/map", params={"bbox": BBOX_SE}).json()

    assert body["type"] == "FeatureCollection" and len(body["features"]) == 1
    feature = body["features"][0]
    assert feature["geometry"]["type"] == "Polygon"
    assert feature["properties"]["display_mode"] == "approximate"
    assert_no_finer_than_cell(body, SE, cells.cell_of(SE, 9))


def test_the_reporter_also_gets_public_precision_on_the_map(client: TestClient) -> None:
    start(client).post("/api/v1/relatos", json=relato())

    body = client.get("/api/v1/map", params={"bbox": BBOX_SE}).json()

    assert_no_finer_than_cell(body, SE, cells.cell_of(SE, 9))


def test_repeated_map_reads_are_identical(client: TestClient, other_client: TestClient) -> None:
    start(client).post("/api/v1/relatos", json=relato())

    reads = {
        str(other_client.get("/api/v1/map", params={"bbox": BBOX_SE}).json()) for _ in range(20)
    }

    assert len(reads) == 1


def test_map_outside_the_bbox_is_empty(client: TestClient) -> None:
    start(client).post("/api/v1/relatos", json=relato())

    body = client.get("/api/v1/map", params={"bbox": "-43.3,-22.95,-43.1,-22.85"}).json()

    assert body["features"] == []


def test_map_too_wide_asks_to_zoom_in(client: TestClient) -> None:
    body = client.get("/api/v1/map", params={"bbox": "-50,-25,-45,-20"}).json()

    assert body["zoom_in"] is True and body["features"] == []


def test_map_rejects_a_malformed_bbox(client: TestClient) -> None:
    response = client.get("/api/v1/map", params={"bbox": "1,2,3"})

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "bbox_invalid"


def test_validation_errors_use_the_same_envelope(client: TestClient) -> None:
    body = relato(kind="party")

    response = start(client).post("/api/v1/relatos", json=body)

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["code"] == "validation_error" and detail["errors"][0]["loc"][-1] == "kind"
