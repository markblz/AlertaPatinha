# Mobile and native path: PWA → store apps without forking the product (verified 2026-10-22)

Method: package versions and dates were pulled live on 2026-10-22 from the npm registry (`dist-tags.latest` plus `time`) and the GitHub releases API. Browser support comes from MDN `@mdn/browser-compat-data` **8.1.7** (published 2026-10-22). Policies and docs were fetched from official pages the same day. I measured bundle sizes myself from the npm tarballs (`gzip -9`, `brotli -q 11`). Anything not verified is labelled **Inference** or listed under Gaps. The baseline is the existing stack: Next.js 16 App Router + React 19 PWA, MapLibre GL JS 6, FastAPI at `/api/v1` proxied same-origin through Next rewrites, and the pnpm/uv monorepo.

### Version snapshot (2026-10-22)

| Thing | Current | Date | Source |
|---|---|---|---|
| next / react | **16.4.2** / **19.3.1** | 2026-10-15 / 2026-10-14 | [npm next](https://www.npmjs.com/package/next), [npm react](https://www.npmjs.com/package/react) |
| maplibre-gl | **6.15.0** | 2026-10-18 | [npm](https://www.npmjs.com/package/maplibre-gl) |
| pmtiles (JS) | 4.5.0 | 2026-08-10 | [npm](https://www.npmjs.com/package/pmtiles) |
| serwist / @serwist/turbopack | 9.5.13 (10.0.0-preview.14 on `preview`) | 2026-10-04 | [npm](https://www.npmjs.com/package/@serwist/turbopack) |
| @capacitor/core, cli, android, ios | **8.5.3** (major 8.0.0 shipped 2025-12-08; **9.0.0-alpha.8** on `next`) | 2026-10-07 | [npm](https://www.npmjs.com/package/@capacitor/core), [GitHub releases](https://github.com/ionic-team/capacitor/releases) |
| @capacitor/push-notifications / camera / geolocation / app / share / browser / preferences | 8.1.3 / 8.2.6 / 8.2.4 / 8.1.2 / 8.0.3 / 8.0.5 / 8.0.1 | Oct 2026 (preferences Feb 2026) | npm |
| @capacitor-firebase/messaging | 8.5.2 | 2026-09-17 | [npm](https://www.npmjs.com/package/@capacitor-firebase/messaging) |
| @capacitor/file-transfer | 2.0.6 | 2026-10-02 | npm |
| @bubblewrap/cli | **1.27.0** | 2026-10-09 | [npm](https://www.npmjs.com/package/@bubblewrap/cli), [releases](https://github.com/GoogleChromeLabs/bubblewrap/releases) |
| android-browser-helper (TWA runtime) | **2.7.4** | 2026-10-02 | [releases](https://github.com/GoogleChrome/android-browser-helper/releases) |
| expo (SDK) | **58.0.17** (SDK 58.0.0 on npm 2026-09-29; announcement post 2026-10-15) | 2026-10-21 | [npm](https://www.npmjs.com/package/expo), [SDK 58 changelog](https://expo.dev/changelog/sdk-58) |
| react-native | **0.88.0** (Expo 58 bundles RN 0.88.0 + React 19.3.0) | 2026-10-15 | [npm](https://www.npmjs.com/package/react-native), `expo@58.0.17/bundledNativeModules.json` |
| expo-router / expo-notifications | 58.0.25 / 58.1.6 | 2026-10-21 | npm |
| react-native-web | 0.21.4 | 2026-10-08 | npm |
| @maplibre/maplibre-react-native | **11.5.0** (MapLibre Native Android 13.6.1 / iOS 6.31.0 since 11.4.0) | 2026-10-04 | [npm](https://www.npmjs.com/package/@maplibre/maplibre-react-native), [releases](https://github.com/maplibre/maplibre-react-native/releases) |
| expo-server-sdk (Node) | 8.0.0 | 2026-10-22 | npm |
| browser-image-compression | 2.0.2, **last published 2023-03-06** (stale) | — | [npm](https://www.npmjs.com/package/browser-image-compression) |

---

## RECOMMENDATION (read first)

### Path order

| Step | What | Trigger | Effort (Inference) | Why |
|---|---|---|---|---|
| **0 (now)** | Strong PWA on Next.js. Public pages are server-rendered with OG tags, Web Push uses VAPID, and an IndexedDB outbox handles offline reports | — | — | Web is the product. About 78% of users are on Android, where Chrome gives Web Push, install and Background Sync with no store involved |
| **1** | **Google Play via Trusted Web Activity** (Bubblewrap 1.27.0), published under the *final* applicationId | The PWA is installable, has an offline fallback, returns no 404/5xx on in-scope URLs, and a Play **organization** account exists | Days | No code fork. It runs in the user's Chrome, so Web Push, Background Sync and the latest engine all work. Notifications are delegated to the app. The APK is tiny. Bubblewrap ≥1.25 already targets API 36, which Play has required since 2026-08-31 |
| **2** | **iOS App Store via Capacitor 8**, bundling a static-exported "app zone", **not** `server.url`. Add native push (APNs/FCM), camera, geolocation, share sheet and Universal Links | iOS metrics justify it, e.g. iOS users don't install to the Home Screen, so push opt-in stalls | Weeks | This is the only posture that defends against Guideline 4.2 ("elevate it beyond a repackaged website") without a rewrite |
| 2b (optional) | Use the same Capacitor project for Android and **replace the TWA under the same applicationId** | Android needs something TWA can't do: background location, native camera UX, offline map packs | Small delta after step 2 | Keeps one native shell. An update in place keeps installs and reviews (Inference) |
| **3 (only if needed)** | Expo SDK 58 / RN 0.88 with @maplibre/maplibre-react-native 11.5 | Native-grade needs: background geofencing, heavy map interaction on low-end devices, offline map packs | Months | The shared packages (below) make this a port, not a rewrite |

**Don't do:**
- **Capacitor `server.url` → live site.** Capacitor's own docs say "**This is not intended for use in production.**" ([config](https://capacitorjs.com/docs/config)). It hits the 4.2 "repackaged website" wording directly, and the app shows a blank error page when offline.
- **PWABuilder iOS.** It is labelled "**Experimental**". It wraps the remote PWA in a WKWebView, so it carries the same 4.2 exposure ([PWABuilder app-store doc](https://raw.githubusercontent.com/pwa-builder/pwabuilder/main/docs/builder/app-store.md)).
- **Replacing Next.js with Expo Router for web.** See Q3.

### Architectural rules to adopt NOW (cheap now, expensive later)

1. **Two rendering zones, enforced by directory boundaries inside `apps/frontend`.**
   - The **public zone** covers `/caso/[id]`, `/relato/[id]`, org pages and the landing page. These are RSC/SSR pages with `generateMetadata` and OG tags, and they exist only on the web server.
   - The **app zone** covers the report flow, map, inbox, settings and auth screens. It is client components only, in a directory such as `src/app-zone/` that must not import `next/headers`, `server-only`, server actions, `cookies()`, or route handlers that read `Request`.
   - Lint-enforce this with eslint `no-restricted-imports` or dependency-cruiser.
   - Do not build the Capacitor shell yet, and do not extract workspace packages yet. The repo's CLAUDE.md says "one frontend app", and "don't create … packages before their milestone". Extract only when a second consumer exists. The boundary is what makes that a one-week job later.
   - The reason is that `output: 'export'` rejects dynamic routes without `generateStaticParams`, Request-reading route handlers, cookies, rewrites, redirects, headers, proxy, ISR, the default image loader, draft mode, server actions and intercepting routes ([Next static exports](https://nextjs.org/docs/app/guides/static-exports)).
2. **All mutations and authorization go through FastAPI `/api/v1`.** No Server Actions, and no Next route handlers acting as a BFF for app-zone features. Server Actions don't exist in a static export or in React Native. One backend owns writes. That is the existing invariant in the core_tech_stack note.
3. **One generated, typed API client with an injected `baseUrl`.** Generate it from FastAPI's OpenAPI with openapi-ts, openapi-typescript or orval.
   - Web uses relative `/api/v1` through the Next rewrite. Native uses an absolute `https://<domain>/api/v1`.
   - The backend CORS allowlist must accept `capacitor://localhost` (iOS) and `https://localhost` (Android). These are Capacitor's defaults: `iosScheme` is `capacitor` and can't be `http`/`https`, and `androidScheme` is `https` ([config](https://capacitorjs.com/docs/config)).
   - The same origins must also be on the **quarantine bucket's CORS** for the presigned upload in photo-pipeline.md. Use WebView `fetch` with FormData, not `CapacitorHttp.request()`, which only takes string or JSON data.
4. **Auth must accept `Authorization: Bearer` from day 1.** ADR-0008's opaque session token can travel either way: as a Bearer header, or as an HttpOnly cookie, which is optional and web-only. Hide token storage behind a `TokenStore` port: an HttpOnly cookie or memory on the web, Keychain/Keystore on native.
   - The reason is that a bundled Capacitor app is cross-site to your API. iOS: "As of iOS 14, you cannot use 3rd party cookies by default" ([Capacitor Cookies](https://capacitorjs.com/docs/apis/cookies)). Android WebView: "Apps targeting LOLLIPOP or later default to disallowing third party cookies" ([CookieManager](https://developer.android.com/reference/android/webkit/CookieManager)).
5. **Platform ports.** Put `push`, `photo` (capture and pick), `location`, `share`, `connectivity`, `persistentStorage`, `deepLink` and `badge` behind interfaces. Ship web adapters now. Feature code never calls `navigator.*` directly. Android System WebView lacks `PushManager`, `SyncManager` and `navigator.share` (BCD: `webview_android=false`), so Capacitor-Android needs different adapters from Chrome/TWA.
6. **URL contract.**
   - Canonical public URLs are stable, on **one host**, and never redirected.
   - A single shared `routeFor(url)` maps a canonical URL (`/caso/123`) to an in-app route. The app zone uses query or client routing (`/app/caso?id=123`) for runtime IDs.
   - Caddy serves `/.well-known/assetlinks.json` and `/.well-known/apple-app-site-association` as `application/json` with no redirect.
   - **Freeze the Android applicationId and the iOS bundle ID now.** They are immutable store identities, and TWA → Capacitor reuse depends on them (Inference).
7. **Provider-agnostic push.** Use a `push_endpoint` table (see Q4) keyed by `(provider, token_hash)`. Payloads are built in the **Declarative Web Push shape** (`web_push: 8030`, `notification.title`, `notification.navigate` = canonical URL), and the service worker parses the same JSON. A notification tap always resolves to a canonical URL, so web, TWA, Capacitor and Expo route identically.
8. **Offline outbox.** IndexedDB records carry a client-generated idempotency key (UUIDv7). Server endpoints are idempotent on that key. Flush with Background Sync where it exists, otherwise on `online`, `visibilitychange` or app resume. Photos are stored as Blobs.
9. **Media rule (consistent with photo-pipeline.md and repo rule 7).**
   - The client reads EXIF GPS and DateTimeOriginal first, as a private `client_exif` hint. It then downsizes and re-encodes to **JPEG**, because Safari iOS can't encode WebP from canvas (Q7). Canvas re-encoding drops the EXIF.
   - The server re-strips and generates derivatives, including a **1200×630 OG JPEG under 300 KB**. Accept HEIC server-side.
   - This works the same in web, TWA and Capacitor (WebView canvas).
10. **Platform-neutral code stays pure TS, in directories now and packages only when a second consumer exists.**
    - This covers zod schemas, enums and the case/report state machines, the generated API client, the i18n catalogs (pt-BR, JSON/ICU) and the map style JSON with **absolute** `pmtiles://https://…` source URLs. None of it may import DOM or Next code.
    - When Expo or a shell app arrives, **pin one React version workspace-wide**: Expo docs say "Duplicate React versions in a single app will cause runtime errors" ([Expo monorepos](https://docs.expo.dev/guides/monorepos/)).
    - MapLibre is lazy-loaded and never on the report flow's critical path.

### Relation to existing decisions (evidence vs decision; decisions win)

| Existing doc | This note says | Status |
|---|---|---|
| ADR-0009 (PWA first; Expo only if iOS push or background location is the bottleneck) | Compatible. Two refinements to consider: (1) a **TWA on Play** is a packaging step, not a native app, and doesn't change PWA-first; (2) if **iOS push** becomes the bottleneck, **Capacitor-iOS** (bundled app zone) is cheaper than Expo. Keep Expo for the **background-location** trigger | Candidate ADR-0009 amendment |
| CLAUDE.md rule 1 ("ONE Next.js PWA") | A Capacitor shell would be a second *build target* of the same frontend code. Not needed now | Needs an ADR when step 2 starts |
| photo-pipeline.md §2 ② "WebP/JPEG q≈0.75–0.8" | Safari iOS has **no WebP canvas encoding** (BCD). Use JPEG on the client, or feature-detect via `blob.type`. Server derivatives stay WebP/AVIF | Correction for the doc owner |
| photo-pipeline.md open question 7 (does iOS file input still convert HEIC to JPEG?) | The Safari 27 beta notes list a fix: "HEIC images were incorrectly converted to JPEG when uploaded via … file input". Expect HEIC from iOS 27; still needs a device test | Partial answer |
| ADR-0008 (opaque in-house sessions) | Stays transport-agnostic: Bearer for native, cookie optional for web | Compatible |

**Key invariant:** every user capability is reachable through `/api/v1` plus a platform port. Only the public SEO/OG zone depends on the Next server runtime.
**Main failure mode:** app-zone code quietly picks up a server-only Next feature (a server action, `cookies()`, a proxy redirect, a `[id]` route). The static export then fails months later, on the day iOS work starts. Mitigation: the lint boundary (rule 1), plus a CI job that runs `next build` with `output: 'export'` on a tiny shell app once rule 1 has a few features.

---

## Q1. Capacitor 8: can it wrap a Next.js 16 App Router app?

### Takeaway
Yes, but only the static-export subset. With (a), a bundled `output: 'export'`, the app zone works if it is client-rendered and talks to an absolute API URL with bearer auth. With (b), `server.url` pointing at the live site, Capacitor itself documents it as not for production, and it invites a 4.2 rejection. Use (a) on iOS. Bearer tokens are the right default for native.

### Cited findings
- **Capacitor 8 requirements:** iOS deployment target 15.0. "Capacitor 8 requires Xcode 26.0+". Android minSdk 24, compile/targetSdk **36**. Node ≥22. Android Studio Otter 2025.2.1+. New iOS projects use **SPM by default**. `android.adjustMarginsForEdgeToEdge` was removed in favour of the SystemBars core plugin plus CSS `env()` — [Updating to 8.0](https://capacitorjs.com/docs/updating/8-0). Release cadence: 8.0.0 2025-12-08, 8.4.0 2026-06-02, 8.5.0 2026-07-31 (added UIScene support), 8.5.3 2026-10-07 — [releases](https://github.com/ionic-team/capacitor/releases), npm.
- **Apple SDK floor:** since 2026-04-28, uploads must be built with **Xcode 26+ / iOS 26 SDK**. Since 2026-09-09, the minimum deployment target is iOS 13 — [Apple upcoming requirements](https://developer.apple.com/news/upcoming-requirements/). Capacitor 8 already meets this.
- **(a) Static export: what breaks.** The [Next.js static exports docs](https://nextjs.org/docs/app/guides/static-exports) (lastUpdated 2026-08-09) list the unsupported features:
  - Dynamic routes with `dynamicParams: true`, or without `generateStaticParams()`.
  - Route Handlers that rely on Request.
  - Cookies, Rewrites, Redirects, Headers, **Proxy** (formerly middleware), ISR.
  - Image Optimization with the default loader. You need a custom `loader`/`loaderFile`.
  - Draft Mode, **Server Actions**, Intercepting Routes.

  What still works: Server Components "run during the build", Client Components with client fetching, and GET route handlers marked `export const dynamic = 'force-static'`.
- Mapping that to this stack:
  - The `/api/v1` rewrite disappears, so the API needs an absolute URL plus CORS.
  - Proxy-based auth gating disappears.
  - RSC request-time data fetching becomes build-time only.
  - `[id]` pages for user content can't be pre-enumerated.
  - `next/image` needs a loader that points at the media CDN.
  - Intercepting-route modals (photo viewers) must become client state.
- **(b) `server.url`:** "Load an external URL in the Web View … **This is not intended for use in production.** … intended for use with live-reload servers". `allowNavigation` and `cleartext` carry the same warning — [Capacitor config](https://capacitorjs.com/docs/config).
- **App Store Guidelines** (page "Last Updated: October 16, 2026") — [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/):
  - **4.2:** "Your app should include features, content, and UI that elevate it beyond a repackaged website. If your app is not particularly useful, unique, or 'app-like,' it doesn't belong on the App Store."
  - **4.2.2:** "apps shouldn't primarily be marketing materials, advertisements, web clippings, content aggregators, or a collection of links."
  - **4.2.3(ii):** downloading extra resources on first launch must be disclosed.
  - **2.5.2:** apps may not "download, install, or execute code which introduces or changes features or functionality of the app". This matters for OTA live updates.
  - **2.5.6:** must use WebKit.
  - **4.5.4:** "Push Notifications must not be required for the app to function".
  - **5.1.1(v):** "If your app supports account creation, you must also offer account deletion within the app".
  - **4.8:** third-party/social login for the primary account requires an equivalent privacy-preserving option.
- **What satisfies reviewers:** Apple publishes no checklist. The only primary-adjacent statement I found is from a Capacitor core team member (2020): using Capacitor "to just load a website will still get your app rejected"; the app "cannot remotely load the web content"; reviewers expect "app like visual design, provide integration into device features, and be accessible without internet" — [Ionic forum](https://forum.ionicframework.com/t/apple-4-2-minimum-functionality/189688). That's an opinion, not policy.
- **Cookies and HTTP in Capacitor WebViews:**
  - iOS: "As of iOS 14, you cannot use 3rd party cookies by default". `WKAppBoundDomains` in Info.plist helps, and "You can add up to 10 domains". The `CapacitorCookies` `document.cookie` patch is off by default — [Cookies](https://capacitorjs.com/docs/apis/cookies).
  - `CapacitorHttp` (off by default) patches `fetch`/XHR to native libraries. On native, direct `request()` data "can only be a string or a JSON". FormData/Blob work only through the patched fetch/XHR. "Parsing and transferring large amount of data from native to the web can cause issues", so use `@capacitor/file-transfer` for files — [Http](https://capacitorjs.com/docs/apis/http).
  - Android WebView third-party cookies default to off for API 21+ apps — [CookieManager](https://developer.android.com/reference/android/webkit/CookieManager).
- **Storage in Capacitor:** "the OS will reclaim local storage from Web Views if a device is running low on space". The same applies to IndexedDB on iOS. Use Preferences for small data and SQLite for larger data — [Storage guide](https://capacitorjs.com/docs/guides/storage). Ionic stopped new sales of its commercial products (Appflow, Identity Vault, Portals) in Feb 2025, and Appflow access lasts until 2027-12-31 — [Ionic blog](https://ionic.io/blog/?p=6282). The community secure-storage plugin `@aparajita/capacitor-secure-storage` is at 8.0.1 (2026-09-23, npm).
- **Edge-to-edge in Capacitor 8 (SystemBars):** on Android WebView < Chromium 140, `env(safe-area-inset-*)` can be wrong. `insetsHandling: 'css'` (the default) injects `--safe-area-inset-*` variables. `'native'` becomes the default in Capacitor 9 — [SystemBars](https://capacitorjs.com/docs/apis/system-bars).

### Inferences
- **Bearer tokens are recommended over cookies for native.** Both WebViews block third-party cookies by default, and `WKAppBoundDomains` is a 10-domain workaround with side effects. Keep an HttpOnly cookie on the web for XSS resistance if you want. Make the API accept both, with the same session table, CSRF protection only on the cookie path, and Bearer for native. Store native tokens in Keychain/Keystore, not `localStorage`, which the OS can reclaim.
- **Shell shape for later:**
  - Create `apps/native-shell`, a thin Next app with `output: 'export'`, `trailingSlash: true` and `images.unoptimized` or a CDN loader. It imports the app-zone packages and is the Capacitor `webDir`.
  - Public pages open via the deep-link → `routeFor()` → client fetch path.
  - Don't try to toggle export mode on the main web app. One server-only route anywhere fails the whole export.
- **4.2 defensible posture:**
  - Bundled assets.
  - Offline-capable report drafting (outbox).
  - Native camera through `@capacitor/camera`, native geolocation with a proper Info.plist purpose string, and native APNs push.
  - Native share sheet and Universal Links.
  - Review notes that explain the civic/emergency use.
  - No external-browser hops for core flows.

  Push alone is unlikely to be enough. A third-party anecdote quotes a reviewer saying push, Core Location and sharing "do not provide a robust enough experience" (unverified secondary source).
- **OTA web updates** (Capgo, `@capgo/capacitor-updater` 8.53.1) sit in a grey zone under 2.5.2. Use them only for bug fixes, never to add features. Gap: Apple's Developer Program License Agreement interpreted-code clause was not fetched.

### Gaps
- No primary Apple data on 4.2 rejection rates for Capacitor apps in 2026.
- I did not test Next 16.4 App Router client navigation (RSC `.txt` payload fetches with `?_rsc=`) under `capacitor://localhost`. Spike before committing.

---

## Q2. Trusted Web Activity for Google Play; PWABuilder for iOS

### Takeaway
TWA via Bubblewrap is alive, actively maintained, and the fastest low-risk Play path for this app. The requirements are a verified `assetlinks.json` (with the **Play App Signing** fingerprint), a sound PWA, an offline fallback and no 404/5xx in scope. Web Push works and shows as the app's notifications, including the Android 13+ permission flow. PWABuilder iOS is experimental and remote-loading, so don't rely on it.

### Cited findings
- **Bubblewrap activity:** 1.25.0 (2026-07-31) raised **targetSdkVersion to 36**. 1.26.0 came 2026-10-08. 1.27.0 (2026-10-09) raised the Node engine to 18 and moved to android-browser-helper 2.7.4 — [Bubblewrap releases](https://github.com/GoogleChromeLabs/bubblewrap/releases), npm times.
- **android-browser-helper:** 2.7.3 (2026-08-12) added "Support `USE_HIGH_PRI_NOTIFICATIONS` manifest metadata for sending high priority notifications for TWA". That is relevant for emergency alerts. 2.7.4 (2026-10-02) merged "WebView fallback full screen" into stable — [releases](https://github.com/GoogleChrome/android-browser-helper/releases).
- **What a TWA is:** it renders with the user's browser, fullscreen, verified by Digital Asset Links. Chrome ≥72 is required. If the browser doesn't support TWA, it falls back to Custom Tabs. "The host app has no direct access to web content, cookies, or localStorage" — [TWA overview](https://developer.chrome.com/docs/android/trusted-web-activity/overview) (last updated 2020-02-04, stale but still the official page).
- **Setup:** `npm i -g @bubblewrap/cli`, then `bubblewrap init --manifest=…`, then `bubblewrap build`. Upload `assetlinks.json` to `/.well-known/assetlinks.json`. "Without verification, the app opens your site as a Custom Tab with browser UI". Google Play may re-sign with another key — [Bubblewrap quick start](https://developer.chrome.com/docs/android/trusted-web-activity/quick-start) (2019-08-28). With Play App Signing, "the certificate fingerprint produced by running keytool locally will usually not match", so take it from Play Console → App signing — [assetlinks guide](https://developer.android.com/training/app-links/configure-assetlinks) (updated 2026-10-16).
- **Quality criteria (Chrome 86+):** failed Digital Asset Links verification at launch, an offline resource with no service worker response (the dino page), and HTTP 404/5xx are treated like app crashes in Android Vitals — [What's new for Web in Play](https://developer.chrome.com/docs/android/trusted-web-activity/whats-new) (2020-12-02), [quality criteria post](https://goo.gle/twa-quality-criteria-update). The same post covers geolocation delegation, which surfaces native permission dialogs.
- **Push in TWA:** `TrustedWebActivityService` "lives in a client app and serves requests from a Trusted Web Activity provider … only serves requests to do with notifications", so notifications are "attributable to the client app and … managed by notification permissions of the client app" — [androidx reference](https://developer.android.com/reference/androidx/browser/trusted/TrustedWebActivityService). android-browser-helper ships `NotificationPermissionRequestActivity` for the Android 13 (T) runtime permission ([source](https://github.com/GoogleChrome/android-browser-helper/blob/main/androidbrowserhelper/src/main/java/com/google/androidbrowserhelper/trusted/NotificationPermissionRequestActivity.java)). Bubblewrap adds `android.permission.POST_NOTIFICATIONS` when `enableNotifications` is set ([FeatureManager.ts](https://github.com/GoogleChromeLabs/bubblewrap/blob/main/packages/core/src/lib/features/FeatureManager.ts)).
- **Play requirements in force:**
  - New apps and updates must target **API 36** from **2026-08-31**, with an extension available to 2026-11-01 — [target SDK](https://developer.android.com/google/play/requirements/target-sdk).
  - Personal developer accounts created after 2023-11-13 need a closed test with "a minimum of 12 testers" "opted in continuously for at least 14 days" before production — [Play Help 14151465](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en).
  - Apps that allow account creation need an in-app deletion path **and** a web link for deletion requests — [Play Help 13327111](https://support.google.com/googleplay/android-developer/answer/13327111?hl=en).
  - **Developer verification goes live 2026-09-30 in Brazil** (with Indonesia, Singapore and Thailand). Play-distributed apps are "automatically registered", but identity verification is still required — [developer verification](https://developer.android.com/developer-verification/guides) (updated 2026-08-18).
- **Play content policy:** the "Webviews and Affiliate Spam" policy targets apps that "provide a webview of a website without permission from the website owner or administrator" ([Spam policy](https://support.google.com/googleplay/android-developer/answer/9899034)). The Limited Functionality policy says "We do not allow apps that only have limited functionality and content", and Broken Functionality says "We don't allow apps that crash, force close, freeze…" ([policy](https://support.google.com/googleplay/android-developer/answer/9898783?hl=en)).
- **PWABuilder iOS:** "creates a native Swift app with a WebView that allows you to load your PWA". It needs macOS + Xcode and the US$99/year developer program. Push works through **FCM** after manual AppDelegate setup. It is labelled **Experimental**, and "acceptance … depends only on UI/UX of your PWA" — [PWABuilder app-store doc](https://raw.githubusercontent.com/pwa-builder/pwabuilder/main/docs/builder/app-store.md). The repo is active (pushed 2026-10-22, [GitHub](https://github.com/pwa-builder/PWABuilder)). PWABuilder's Android output is Bubblewrap-based.

### Inferences
- A TWA of your own DAL-verified domain doesn't fall under the webview-spam clause, because you are the site owner. The real Play risk is the quality bar, which a Serwist offline fallback plus no in-scope 404s satisfies.
- **Use an organization Play account.** The 12-tester/14-day rule text names only personal accounts. Organization accounts need a D-U-N-S number (not re-verified this session).
- TWA runs in Chrome, so Background Sync, Web Push, WebGL2 for MapLibre v6 and the cookie/session state all behave exactly as on the mobile web. The WebView fallback (no TWA-capable browser) loses Web Push and Background Sync (BCD `webview_android=false`). That is acceptable as a degraded mode.
- Lighthouse: the current official pages state no numeric score requirement. Treat the Chrome 86 crash criteria plus installability as the bar.
- Keep `assetlinks.json` multi-target from the start. Include the Play App Signing SHA-256 plus the upload key, and later a Capacitor build if its package differs.

### Gaps
- I did not re-verify whether the Chrome 86 "crash" enforcement still applies in 2026 (the source is from 2020).
- I did not verify which non-Chrome Android browsers (Samsung Internet, Edge, Firefox) support the TWA protocol in 2026.
- The Lighthouse performance minimum from early TWA docs was not re-verified.

---

## Q3. Expo / React Native as the alternative, and what to share

### Takeaway
Expo SDK 58 (RN 0.88, React 19.3, iOS 16.4+, Android 7+) is a viable later port. Share types, the OpenAPI client, zod schemas, domain logic, i18n catalogs and the map style JSON. Don't share UI or routing. Keep Next.js for the web. `@maplibre/maplibre-react-native` 11.5 is native-only (Android/iOS), New-Architecture-only, needs a dev build, and reads the same style JSON and PMTiles if source URLs are absolute.

### Cited findings
- **SDK 58 support table:** RN **0.88**, Min Android **7+**, compileSdk **37**, targetSdk **36**, Min iOS **16.4+**, Min Xcode **26.4+** — [Expo versions](https://docs.expo.dev/versions/latest/). The changelog post (2026-10-15) says RN went "from 0.86 to 0.88". It also says Expo Router **data loaders, SSR and middleware are stable**, and web output defaults to `"server"` when `web.output` is unset — [SDK 58](https://expo.dev/changelog/sdk-58).
- **Expo Router on web:** static output is required for SEO in static mode. SDK 58 adds `generateMetadata()` for metadata present before JS runs, while `<Head>` now only updates after hydration. Static mode needs `generateStaticParams` for dynamic routes. `apiRoutes: true` requires a deployed server — [static rendering](https://docs.expo.dev/router/web/static-rendering/).
- **DOM components (`'use dom'`):** run React DOM code inside a WebView in the native app. This "enables incremental migration for an entire website to a universal app by moving on a per-component basis". Limits: SPA only, "no SSR, SSG, or React Server Components", serializable props, no `children`, and standard JS is "slower to parse and start up than optimized Hermes bytecode" — [DOM components](https://docs.expo.dev/guides/dom-components/).
- **Monorepo:**
  - Metro is configured automatically for monorepos since SDK 52.
  - pnpm isolated installs are supported since SDK 54, with fallback `nodeLinker: hoisted`.
  - `workspace:*` dependencies work.
  - "Duplicate React Native versions in a single monorepo are not supported", and "Duplicate React versions in a single app will cause runtime errors".
  - Autolinking module resolution is on by default for monorepos from SDK 55.

  Source: [Expo monorepos](https://docs.expo.dev/guides/monorepos/).
- **Push on Expo:** Expo Go lost push support in SDK 53, so you need a development build — [push FAQ](https://docs.expo.dev/push-notifications/faq/).
- **@maplibre/maplibre-react-native:**
  - It is described as "React Native library for creating maps with MapLibre Native for Android & iOS" and is MIT licensed — [repo](https://github.com/maplibre/maplibre-react-native).
  - Requirements: RN ≥0.80. "From v11 onwards only the new architecture is supported". Android API ≥23. MapLibre Native Android 13.6.1 / iOS 6.31.0 — [getting started](https://maplibre.org/maplibre-react-native/docs/setup/getting-started).
  - Expo: add the `@maplibre/maplibre-react-native` config plugin. "This package can't be used with 'Expo Go'" — [Expo setup](https://maplibre.org/maplibre-react-native/docs/setup/expo).
  - v11.0.0 shipped 2026-04-17. Peer deps: `expo >=54`, `react-native >=0.80` (npm).
- **PMTiles on MapLibre Native:** "Starting MapLibre Android 11.7.0, PMTiles archives are supported … Prefix any tile source URL with `pmtiles://`" (`pmtiles://https://…`, `pmtiles://file://…`, `pmtiles://asset://…`). "MapLibre Native requires the URL inside `pmtiles://` to be fully specified", and "PMTiles sources do not support offline pack downloads or caching" — [MapLibre Native Android PMTiles doc](https://github.com/maplibre/maplibre-native/blob/main/platform/android/docs/data/PMTiles.md). The MapLibre newsletter credits Android 11.8.0 / iOS 6.10.0 with "the new PMTiles support" ([Jan 2025 newsletter](https://maplibre.org/news/2025-02-03-maplibre-newsletter-january-2025/)). Either way, RN 11.5's 13.6.1/6.31.0 includes it.
- **GL JS v6 still needs the protocol registered:** `maplibregl.addProtocol('pmtiles', protocol.tile)` with the `pmtiles` package — [MapLibre example](https://www.maplibre.org/maplibre-gl-js/docs/examples/pmtiles-source-and-protocol/), [Protomaps docs](https://docs.protomaps.com/pmtiles/maplibre).

### What to share (Inference, grounded in the above)

| Share (pure TS, no DOM/RN imports) | Don't share |
|---|---|
| OpenAPI-generated types + fetch-based client (`baseUrl`, auth header injection) | Screens and components (DOM vs RN primitives) |
| zod schemas (form validation + API parsing), enums, case/report state machines | Routing (Next App Router vs Expo Router) |
| Domain logic: distance/H3 helpers, status rules, formatting (pt-BR dates/numbers via `Intl`) | Map component (`maplibre-gl` + react-map-gl vs `@maplibre/maplibre-react-native`) |
| i18n catalogs (JSON/ICU) + a runtime that works in both, e.g. i18next or FormatJS (verify RN `Intl` coverage on Hermes) | Push/camera/location adapters (one per platform) |
| Map **style JSON**, with absolute `pmtiles://https://…` URLs, plus GeoJSON contracts | Service worker / outbox *transport* (keep the outbox *record schema* shared) |
| Design tokens (colors, spacing) as plain objects | CSS |

- **Expo Router web vs keeping Next.js:** keep Next.js.
  - The team baseline is already Next.
  - RSC keeps first-load JS small on low-end Android.
  - Next's metadata path already treats WhatsApp as an HTML-limited bot (Q6).
  - maplibre-react-native has no web target, so a universal app would still need a separate web map.
  - react-native-web adds runtime weight to every page (not measured).

  Revisit only if a single team must own one universal codebase.

### Gaps
- I did not measure the react-native-web/Expo Router web bundle cost against the Next RSC pages.
- I did not verify Hermes `Intl` completeness for pt-BR plural and date formats in RN 0.88.
- Background geolocation/geofencing on Expo 58 (`expo-location` + `expo-task-manager`) and its Play/App Store policy implications were not researched.

---

## Q4. Push across platforms and the backend `push_endpoint` model

### Takeaway
Use one backend table with a `provider` discriminator: `webpush | fcm | apns | expo`.
- Web Push (VAPID) covers Android Chrome, TWA and installed iOS PWAs (16.4+).
- Capacitor-Android needs FCM, because Android WebView has no PushManager. Capacitor-iOS needs APNs, or FCM via the Firebase plugin.
- Expo can use its free relay or raw FCM/APNs tokens.

Build payloads in the Declarative Web Push shape so one notification spec renders everywhere.

### Cited findings
- **Web Push support (BCD 8.1.7):** `PushManager` is in Chrome Android 42+, Samsung Internet 4+, Firefox Android 48+ and Safari iOS 16.4+. **Android WebView: no.** `window.pushManager` (declarative) is in Safari iOS 18.4+. `showNotification` on iOS carries the note "Notifications are supported in web apps saved to the home screen".
- **iOS rules:**
  - "A web app that has been added to the Home Screen can request permission to receive push notifications". The request must be "in response to direct user interaction".
  - The manifest `display` must be standalone/fullscreen.
  - No Apple Developer Program membership is needed. Allowlist `*.push.apple.com`.
  - The Badging API is available.

  Source: [WebKit, Web Push for iOS 16.4](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/) (2023-02-16). Since iOS/iPadOS 26, "By default, every website added to the Home Screen opens as a web app" ([WebKit WWDC25](https://webkit.org/blog/16993/news-from-wwdc25-web-technology-coming-this-fall-in-safari-26-beta/), 2025-06-09).
- **Apple's Web Push server rules:**
  - "Safari doesn't support invisible push notifications … If you don't [show one], Safari revokes the push notification permission".
  - The VAPID public key "must match the public key you provided to `PushManager.subscribe`".
  - "Don't refresh your JWT more frequently than once per hour".
  - Headers: TTL (up to 30 days), Topic (≤32 chars, coalescing), Urgency (`very-low|low|normal|high`).
  - 410 means "The device token has expired".

  Source: [Apple: Sending web push notifications](https://developer.apple.com/documentation/usernotifications/sending-web-push-notifications-in-web-apps-and-browsers).
- **Declarative Web Push (iOS/iPadOS 18.4):** `"web_push": 8030` plus a `notification` object with a required `title` and `navigate`, and optional `body`, `lang`, `dir`, `silent` and `app_badge`. No service worker is needed to subscribe. Older browsers handle the same message in their SW JS — [WebKit, Meet Declarative Web Push](https://webkit.org/blog/16535/meet-declarative-web-push/) (2025-03-27).
- **Capacitor push:** "On iOS it contains the APNS token. On Android it contains the FCM token". Android needs only `google-services.json`. When targeting SDK 33 you must call `checkPermissions()`/`requestPermissions()` — [push-notifications](https://capacitorjs.com/docs/apis/push-notifications). `@capacitor-firebase/messaging` 8.5.2 is the community route to FCM tokens on both platforms (npm; behavior not re-verified).
- **Expo push:**
  - The service is free: "There is no cost associated with sending notifications through Expo push notification service".
  - Limits: 600 notifications/s per project and 100 messages per request. Tokens look like `ExponentPushToken[…]`.
  - Receipts arrive within about 15 minutes and are kept for 24 hours. On `DeviceNotRegistered`, stop sending.
  - Alternatively, use `getDevicePushTokenAsync` to send directly through FCM/APNs.

  Sources: [FAQ](https://docs.expo.dev/push-notifications/faq/), [sending](https://docs.expo.dev/push-notifications/sending-notifications/), [custom](https://docs.expo.dev/push-notifications/sending-notifications-custom/).
- **FCM:** the legacy HTTP/XMPP APIs were deprecated 2023-06-20 and their shutdown began 2024-07-22, so HTTP v1 with OAuth2 is the only path — [Firebase migrate-v1](https://firebase.google.com/docs/cloud-messaging/migrate-v1).
- **TWA:** Web Push is delegated to the app's notifications, and there is a high-priority option in android-browser-helper 2.7.3 (Q2).

### `push_endpoint` model (Inference, derived from the requirements above)

```
push_endpoint
  id                uuid pk
  installation_id   uuid not null        -- client-generated per install/browser profile
  user_id           uuid null            -- anonymous-first: endpoint may predate login
  provider          enum('webpush','fcm','apns','expo') not null
  token             text not null        -- webpush: endpoint URL; fcm/apns/expo: device token
  token_hash        bytea not null       -- sha256(token); UNIQUE(provider, token_hash)
  -- webpush only
  p256dh            text null
  auth_secret       text null
  vapid_key_id      text null            -- subscription is bound to the applicationServerKey; needed for key rotation
  content_encoding  text null            -- 'aes128gcm'
  expiration_time   timestamptz null     -- from PushSubscription.expirationTime
  -- native only
  app_id            text null            -- Android applicationId / iOS bundle id (= APNs topic)
  apns_environment  enum('sandbox','production') null
  -- context
  platform          enum('android','ios','desktop') not null
  surface           enum('browser','installed_pwa','twa','capacitor','expo') not null
  locale            text not null default 'pt-BR'
  app_version       text null
  created_at, last_seen_at, last_success_at timestamptz
  failure_count     int not null default 0
  disabled_at       timestamptz null
  disabled_reason   text null            -- webpush 404/410, APNs 410/BadDeviceToken, FCM UNREGISTERED, Expo DeviceNotRegistered
```
- Keep preferences (watch areas, categories, quiet hours) in separate tables keyed by `user_id`/`installation_id`, not on the endpoint.
- Never put exact locations or PII in payloads. Apple 4.5.4 says push "should not be used to send sensitive personal or confidential information". Send a canonical `navigate` URL and let the app fetch the details.
- One sender interface, with an adapter per provider: pywebpush for webpush, FCM HTTP v1, APNs HTTP/2 (token auth), and Expo.

### Gaps
- No Brazil-specific delivery-rate data for Web Push vs FCM.
- I did not verify whether `@capacitor-firebase/messaging` 8.5.2 returns FCM tokens on iOS without extra AppDelegate work.

---

## Q5. Deep links: App Links + Universal Links from the same domain

### Takeaway
Serve both association files from every host you share links on, with HTTPS, a valid certificate, `application/json`, and **no redirects**. Shared canonical URLs then open the app when it's installed and fall back to the web page automatically. Keep one canonical host and never redirect the shared paths.

### Cited findings
- **Apple:**
  - Place `apple-app-site-association` (no extension) at `https://<fqdn>/.well-known/apple-app-site-association`. "You must host the file using https:// with a valid certificate and with no redirects".
  - Each subdomain needs its own file and entitlement entry. Use `applinks:` entries, with `*.` allowed for subdomains.
  - The format is `applinks.details[].appIDs` + `components` (`/`, `?`, `#`, `exclude`).
  - Since iOS 14, devices fetch the file through **Apple's CDN**. The CDN requests your file "within 24 hours", and "Devices check for updates approximately once per week after app installation". Use `?mode=developer` while developing.
  - "Users who don't download the app get the same information in a web browser instead of the native app".

  Source: [Supporting associated domains](https://developer.apple.com/documentation/xcode/supporting-associated-domains).
- **Android:**
  - Place `https://domain/.well-known/assetlinks.json`. It "must be accessible over an HTTPS connection", "without any redirects", and served with "content-type application/json". Publish it on each host.
  - `sha256_cert_fingerprints` supports multiple values, and you should use the Play App Signing fingerprint.
  - The intent filter needs `android:autoVerify="true"` + VIEW/DEFAULT/BROWSABLE + https + host.
  - Android 15+ adds **dynamic App Links** via `relation_extensions.dynamic_app_link_components`. These "cannot expand the scope" of manifest rules, and Android 14 and older ignores them.

  Sources: [configure assetlinks](https://developer.android.com/training/app-links/configure-assetlinks), [Capacitor deep links](https://capacitorjs.com/docs/guides/deep-links).
- **Capacitor:** listen for `App.addListener('appUrlOpen', …)`, extract the path, and route it — [deep links](https://capacitorjs.com/docs/guides/deep-links).
- **Next.js metadata** supports `itunes: { appId, appArgument }` for the Safari Smart App Banner and `appLinks` (`al:*`) tags — [generateMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata).

### What the web must serve (Inference)
- Serve `/.well-known/assetlinks.json` with all package/fingerprint targets: TWA now, plus Capacitor if its package differs. Serve `/.well-known/apple-app-site-association` with `components` that include `/caso/*`, `/relato/*` and `/o/*`, and exclude `/api/*`, `/admin/*` and auth callbacks. Have **Caddy** serve both statically with a forced `Content-Type: application/json`. Don't rely on Next's `public/` MIME guessing for the extensionless file.
- Canonical shared URLs must render a complete server-side page, which is the fallback when the app isn't installed. Never interpose redirect or tracking hops on shared links. Universal Links require the tapped URL's host to be the associated one.
- Point the in-app router at the shared `routeFor(url)`. Unknown paths open the same URL in the in-app browser or the system browser.
- Once the iOS app exists, add the Smart App Banner on iOS Safari. For Android, the TWA/App Link handles it.

### Gaps
- I did not verify whether WhatsApp (Android/iOS) opens tapped links in a way that triggers App Links/Universal Links rather than an in-app browser. Test on real devices.
- I did not re-check Apple's AASA file-size limit.

---

## Q6. WhatsApp link previews

### Takeaway
Previews need `og:title`, `og:description` and `og:url` in a server-rendered `<head>`, within the first 300 KB of the HTML. `og:image` should be an absolute URL, at least 300 px wide, under 600 KB (target **under 300 KB**), with an aspect ratio of 4:1 or less. So `/caso/[id]` and `/relato/[id]` **must be SSR/SSG**. A client-only page shows no preview. Next 16.4 already serves blocking (non-streamed) metadata to the WhatsApp crawler.

### Cited findings
- WhatsApp's official link-preview spec ([WhatsApp Business Platform: Link previews](https://developers.facebook.com/documentation/business-messaging/whatsapp/link-previews/), [legacy mirror](https://developers.secure.facebook.com/docs/whatsapp/link-previews)):
  - "The og:title, og:description and og:url mark-ups must be inside the `<head>` tag. They should not be empty."
  - og:title should be "without any branding". og:description: "80 characters will suffice".
  - og:url should be "undecorated, without session variables, user identifying parameters and counters".
  - og:image: "This image should be under 600KB in size". "Image should be 300px or more in width … 4:1 width/height or less aspect ratio".
  - "The `<head>` containing the HTML mark-ups must appear within the first 300KB of the HTML".
  - "WhatsApp crawls the web page via an HTTP GET request". The User-Agent is `WhatsApp/2.x.x.x A|I|N`, and `Accept-Language` reflects the recipient's language.
- Third-party field reports say thumbnails show reliably only up to about 300 KB — [Branch FAQ](https://help.branch.io/faq/docs/why-are-some-quick-link-thumbnails-not-shown-in-whatsapp), [Wix](https://support.wix.com/en/article/recommended-social-share-image-size) (secondary).
- **Next.js streaming metadata:** for "HTML-limited bots that can't execute JavaScript … metadata continues to block page rendering … available in the `<head>` tag" — [generateMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata) (lastUpdated 2026-08-19). In **v16.4.2** `HTML_LIMITED_BOT_UA_RE` includes `WhatsApp`, `facebookexternalhit`, `Twitterbot`, `LinkedInBot`, `Slackbot`, `Discordbot` and others (case-insensitive) — [html-bots.ts @ v16.4.2](https://github.com/vercel/next.js/blob/v16.4.2/packages/next/src/shared/lib/router/utils/html-bots.ts). You can override it with `htmlLimitedBots`. `metadataBase` resolves relative OG URLs, and a relative URL without it is a build error.

### Inferences
- **OG image recipe:** a 1200×630 JPEG (1.91:1, within 4:1), quality around 0.7–0.8, kept under 300 KB, generated server-side from the sanitized photo. Use an immutable, versioned CDN URL and declare `og:image:width/height/alt`.
- **The OG image is public.** It must never show an exact-location map, EXIF or faces beyond the policy. This aligns with ADR-0004 (no public exact pins).
- **Caching:** WhatsApp documents nothing. The UA's `A|I|N` suffix (client platform) suggests the *sender's client* fetches the preview at send time. Already-sent previews are then frozen and can't be purged, so get the first render right and make case pages CDN-cacheable and fast.
- Telegram is the second sharing channel in Brazil. Its crawler UA is reported to contain "TwitterBot", which the regex would match. Verify, or extend `htmlLimitedBots`.

### Gaps
- Crawler timeout, redirect-following behaviour and WebP/AVIF acceptance for `og:image` are undocumented by WhatsApp.
- No official statement on preview caching.

---

## Q7. Mobile web UX technical checklist (2026)

Support data is from BCD 8.1.7 unless another source is given.

| Item | Finding | Do |
|---|---|---|
| `viewport-fit=cover` | Chrome Android **135** made Chrome edge-to-edge. `viewport-fit=cover` extends the viewport so the bottom "chin" never shows. `safe-area-inset-bottom` updates as the chin moves, so don't put it in `padding-bottom` because that causes layout thrash. Use `bottom: env(safe-area-inset-bottom)` with `safe-area-max-inset-bottom` (Chrome 135+) and a 36 px fallback — [Chrome edge-to-edge guide](https://developer.chrome.com/docs/css-ui/edge-to-edge). BCD: `viewport-fit` Chrome Android 135, Safari iOS 11 | Set it via Next's `viewport` export. Pad fixed bottom bars and bottom sheets with the max-inset pattern |
| `env(safe-area-inset-*)` | Chrome Android 69+, Safari iOS 11+. Capacitor 8 SystemBars injects `--safe-area-inset-*` for WebView < Chromium 140 | Use `var(--safe-area-inset-bottom, env(safe-area-inset-bottom))` so the native wrapper works |
| `dvh`/`svh`/`lvh` | Chrome Android 108+, Safari iOS 15.4+, Samsung 21+ | Map container `height: 100dvh` (fallback `100vh`). Use `svh` for layouts that must not jump with the URL bar |
| Keyboard | `interactive-widget=resizes-content` works in Chrome Android 108+ and Firefox Android 133+, **not Safari**. VirtualKeyboard API and `env(keyboard-inset-*)` are Chromium-only | Keep the report form out of a fixed bottom sheet when the keyboard is up. Navigate to a full-height step instead |
| Touch targets | Android: at least 48×48 dp with ≥8 dp spacing ([Google accessibility help](https://support.google.com/accessibility/android/answer/7101858)). Material's `minimumInteractiveComponentSize` is 48 dp ([Compose ref](https://developer.android.com/reference/kotlin/androidx/compose/material/minimumInteractiveComponentSize.modifier)). WCAG 2.2 **2.5.8 (AA)**: at least 24×24 CSS px or the spacing exception ([W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)) | Default to 48 CSS px for primary actions and map controls |
| Bottom sheet over map | `overscroll-behavior` in Chrome 63+ (full from 144) and Safari iOS 16+ (partial). `<dialog>` in Chrome 37+ and Safari iOS 15.4+. `popover` in Safari iOS 17+ | Peek / half / full snap states. `overscroll-behavior: contain` on the sheet scroller. The map is `inert` while the sheet is full. Back button closes the sheet via the history state (Inference) |
| Photo input | `capture` is supported on Chrome Android 25+ and Safari iOS 10+ and ignored on desktop. MDN: `environment` means the "outward-facing camera" ([MDN capture](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/capture)). A third-party report says `capture` forces camera-only with no gallery, and that a plain file input on Android 14/15 Chrome lost the camera option ([addpipe](https://blog.addpipe.com/html-file-input-accept-video-camera-option-is-missing-android-14-15/), secondary). Safari 27 beta fixed "HEIC images were incorrectly converted to JPEG when uploaded via … file input" ([WebKit WWDC26](https://webkit.org/blog/17967/news-from-wwdc26-webkit-in-saf), 2026-06-08) | **Two buttons**: "Tirar foto" (`accept="image/*" capture="environment"`) and "Escolher da galeria" (`accept="image/*"`, no capture). Expect HEIC from iOS and handle it server-side |
| Geolocation | `Permissions.query` works in Safari iOS 16+ and Chrome Android 43+ | Ask only after a user tap ("Usar minha localização"), with a pre-explanation. Always offer a manual pin or address. Use `maximumAge` to reuse recent fixes and a timeout of about 10 s. In TWA, location is delegated to native dialogs (Q2). In Capacitor, add Info.plist usage strings |
| Image compression | This corrects photo-pipeline.md ②. `toBlob`/`convertToBlob` **WebP encode: Chrome yes, Safari iOS no**. OffscreenCanvas + `convertToBlob` in Safari iOS 16.4+ and Chrome 69+. `createImageBitmap` in Safari iOS 15+. BCD has no AVIF-encode entry. `browser-image-compression` was last published 2023-03-06 | Write a small in-house helper: `createImageBitmap(file, {imageOrientation:'from-image'})`, scale to about 1600 px long edge, then `image/jpeg` at q≈0.75 in a worker. Check `blob.type`, because an unsupported type silently falls back to PNG (Inference from the spec). Do WebP/AVIF derivatives server-side |
| Outbox + Background Sync | `SyncManager`: Chrome Android 49+ and Samsung 5+. **Not** in Safari iOS, Firefox, or Android WebView. Periodic Sync and Background Fetch are Chromium-only | Use an IndexedDB outbox. Flush on `sync` where supported, else on `online`, `visibilitychange` or app resume, with server idempotency keys |
| Storage durability | Safari's 7-day cap deletes script-writable storage (IndexedDB, LocalStorage, SW caches) after 7 days of use with no interaction. "Web applications added to the home screen … have their own counter" ([WebKit 2020](https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/)). Safari 17: up to 60% of disk per origin, LRU origin eviction, and `persist()` granted by heuristics such as Home Screen use ([WebKit 2023](https://webkit.org/blog/14403/updates-to-storage-policy/)). `StorageManager.persist` in Safari iOS 15.2+ | Call `navigator.storage.persist()` after the first report. Keep outbox items small. Never treat IndexedDB as the source of truth |
| Data saver (prepaid) | `NetworkInformation.saveData` in Chrome Android 65+ and Samsung; not Safari | With Save-Data on, don't auto-load the map or full-resolution photos. Default to a list view |
| Core Web Vitals | Good thresholds: LCP ≤2.5 s, INP ≤200 ms, CLS ≤0.1, at the **p75** of page loads, split mobile/desktop — [web.dev vitals](https://web.dev/articles/vitals) | Track these with RUM (web-vitals), segmented to Android low-end |
| Budget reference | The "Performance Inequality Gap, 2026" (2025-11-24) uses a P75 reference of a Galaxy A24 4G-class phone (Helio G99) on 9/3 Mbps with 100 ms RTT. **Brazil P75 is 12/4 Mbps, 60 ms**. The 3 s budget is 2.0 MiB total with 0.3 MiB JS (JS-light), or 1.2 MiB with 0.62 MiB JS (JS-heavy) — [infrequently.org](https://infrequently.org/2025/11/performance-inequality-gap-2026/) | Set internal CI budgets well below these, because CPU cost dominates on low-end phones (Inference): about 170 KB gz first-load JS on the report route and about 100 KB on public case pages |
| MapLibre size (measured) | `maplibre-gl@6.15.0` `dist/maplibre-gl.mjs` is 1,098,062 B → **291,657 B gzip** / 239,563 B brotli. The worker loads separately: 518,806 B → **146,664 B gzip** / 121,564 B brotli. CSS is 71,596 B → 10,180 B gzip. `pmtiles@4.5.0` ESM is 14,882 B → 5,472 B gzip. v6 is ESM-only and **requires WebGL2** ([v6.0.0 release](https://github.com/maplibre/maplibre-gl-js/releases/tag/v6.0.0)). WebGL2 is in Chrome Android 58+ and Safari iOS 15+ | The main MapLibre chunk alone is about 0.28 MiB gz, close to the whole 3 s JS-light budget. Load it with `next/dynamic(..., { ssr:false })` inside a Client Component (`ssr:false` is "not supported in Server Components", [Next lazy loading](https://nextjs.org/docs/app/guides/lazy-loading)), after first paint or on intent. Show a static map image or list first, and fall back on a WebGL2 init `error` |

---

## Gaps (consolidated)

- I found no 2026 primary data on App Store 4.2 outcomes for Capacitor apps. Apple's Developer Program License Agreement interpreted-code clause (for OTA updates) was not fetched.
- Brazil alternative iOS distribution: since iOS 26.5 (announced 2026-06-18), Brazilian users get alternative marketplaces with **notarization** ("less comprehensive than App Review") and a 5% Core Technology Commission — [Apple newsroom](https://www.apple.com/newsroom/2026/06/apple-announces-changes-to-ios-in-brazil/). I did not verify whether notarization in Brazil skips 4.2 or whether web distribution is allowed. This could become an escape hatch if App Review rejects the app.
- Several TWA docs are from 2019–2021. I did not re-verify the current enforcement of the Chrome 86 quality criteria or which non-Chrome browsers support TWA.
- WhatsApp: crawler timeout, redirects, cache and in-app link handling (App Links/Universal Links from inside WhatsApp) are undocumented. They need device tests.
- I didn't check Safari 27 release notes for Web Push or Home Screen changes beyond the WWDC26 beta post. No webkit.org source found for AVIF/WebP canvas encoding in Safari 27.
- I did not spike Next 16.4 static export under `capacitor://localhost` (RSC payload fetches, `trailingSlash`, 404 handling).
- Apple HIG 44 pt touch target and the Play organization-account D-U-N-S requirement were not re-fetched this session.
- I measured MapLibre size from the npm dist with gzip/brotli. Real chunk sizes depend on Turbopack output and HTTP compression level.
