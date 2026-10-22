# geo — Local

**Milestone:** M1 · **Owns schema:** `geo` · **May depend on:** nothing (callers pass the viewer in)

## Responsibility
Pure location policy: privacy classification, stable display geometry (H3), viewer-tier masking, private zones, `location_access_log`.

## Public surface (`public.py`)
- `mask_for_write(session, point, reporter_id, kind, flags) -> (PrivacyClass, Display)` — write time, stable
- `render_public(facts) -> LocationView` — map/realtime; raises `PrivacyViolation` if exact
- `render_for(session, facts, viewer, context, purpose) -> LocationView` — logs every exact read
- Types: `Point`, `Viewer`, `Tier`, `AccessContext`, `ObservationGeoFacts`, `LocationView`, `RelatoKind`, `AnimalFlag`, `PrivacyClass`, `DisplayMode`; helpers `cell_of`, `ring_of`
- 🧠 `domain/policy.py` (`classify_privacy`, `display_for`, `can_see_exact`, `view_for`) — owner implements; tests `tests/geo/test_policy.py`

## Invariant
No response lets a viewer locate a point more precisely than their access allows — alone or combined. Spec: docs/domain/location-privacy.md.

## Layout
`public.py` → `service.py` → `repository/` (ORM models, queries) → `domain/` (pure logic). Enforced by the `modules-are-layered` import contract.
