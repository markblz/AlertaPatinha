"""Print the OpenAPI document. `make api-contract` writes it to the frontend,
where openapi-typescript turns it into the typed client (web now, native later)."""

import json

from api.main import app


def render() -> str:
    return json.dumps(app.openapi(), indent=2, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    print(render(), end="")
