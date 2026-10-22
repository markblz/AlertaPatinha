import hashlib
import secrets
import uuid
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Principal:
    """Who is making the request. `actor_id` is stable across devices once
    verified (M4); never expose it publicly (it would link a reporter's trail)."""

    actor_id: uuid.UUID
    tier: int
    is_staff: bool = False


@dataclass(frozen=True, slots=True)
class IssuedSession:
    principal: Principal
    token: str  # shown once; only its hash is stored


def new_token() -> str:
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> bytes:
    # A fast hash is enough: the token has 256 bits of entropy (no brute force),
    # and a DB leak must not hand out usable bearer tokens.
    return hashlib.sha256(token.encode()).digest()
