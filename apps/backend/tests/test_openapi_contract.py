from pathlib import Path

import pytest

from api.export_openapi import render

CONTRACT = Path(__file__).resolve().parents[2] / "frontend" / "core" / "api" / "openapi.json"


def test_frontend_contract_matches_the_api() -> None:
    if not CONTRACT.exists():
        pytest.skip("frontend checkout not present")
    assert CONTRACT.read_text() == render(), "API changed: run `make api-contract`"
