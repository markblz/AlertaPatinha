# ADR-0009 — PWA first; native app only if iOS push becomes the bottleneck

**Status:** accepted · 2026-10-21 · amended by [ADR-0011](0011-mobile-first-native-ready.md) (store path: TWA → Capacitor iOS → Expo only for native-grade needs)

## Context
Brazil is ~78% Android / 22% iOS; 65% of internet users are mobile-only, 52%
prepaid, 39% ran out of data in 3 months. A store install is friction before
the first relato. iOS delivers Web Push only to home-screen-installed PWAs;
Background Sync is Chromium-only.

## Decision
- Next.js PWA (manifest now; Serwist service worker + Web Push in M3).
- Offline: IndexedDB **outbox** with idempotency keys (works on Safari too), not Background Sync.
- Performance budget for low-end Android; data-light (client-side photo compression, PMTiles, AVIF/WebP variants).
- Reconsider Expo/React Native only if iOS push opt-in or background location becomes the measured growth bottleneck.

## Consequences
One codebase; shareable links open instantly from WhatsApp; iOS push requires
an install prompt flow.
