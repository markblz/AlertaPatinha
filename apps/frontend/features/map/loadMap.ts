import type { ControlPosition, Map as MapLibreMap, MapOptions } from "maplibre-gl";

import { KINDS } from "@/core/relato/vocabulary";

export const BRAZIL_CENTER: [number, number] = [-51.9, -14.2];
export const DEV_STYLE_URL = "https://tiles.openfreemap.org/styles/liberty";

export function styleUrl(): string {
  return process.env.NEXT_PUBLIC_MAP_STYLE_URL || DEV_STYLE_URL;
}

/**
 * maplibre-gl is ~290 KB gzipped: load it after first paint, never in the shell.
 * Returns null if `signal` aborted while loading: constructing a second map on
 * a container another (soon removed) map is using breaks its positioning.
 */
export async function loadMap(
  options: Omit<MapOptions, "style">,
  signal: AbortSignal,
  attribution: ControlPosition = "bottom-right",
): Promise<MapLibreMap | null> {
  const [{ AttributionControl, Map, getVersion, setWorkerUrl }] = await Promise.all([
    import("maplibre-gl"),
    import("maplibre-gl/dist/maplibre-gl.css"),
  ]);
  // Copied by scripts/copy-maplibre-worker.mjs (bundlers don't emit it).
  setWorkerUrl(`/maplibre/maplibre-gl-worker.${getVersion()}.mjs`);
  if (signal.aborted) return null;
  const map = new Map({
    style: styleUrl(),
    attributionControl: false,
    dragRotate: false,
    pitchWithRotate: false,
    touchPitch: false,
    ...options,
  });
  // OSM attribution must stay visible; screens with bottom actions move it up.
  map.addControl(new AttributionControl({ compact: true }), attribution);
  // Compact attribution opens expanded on first render; collapse it (the "i" reopens it).
  map.once("load", () =>
    map.getContainer().querySelector(".maplibregl-compact-show")?.classList.remove("maplibregl-compact-show"),
  );
  return map;
}

const KIND_COLOR = [
  "match",
  ["get", "kind"],
  ...Object.entries(KINDS).flatMap(([kind, info]) => [kind, info.color]),
  "#4a4f6a",
] as unknown as string;

/** Approximate = hex outline + light fill, no centre dot (location-privacy.md § Map visual language). */
export function addRelatoLayers(map: MapLibreMap): void {
  map.addSource("relatos", {
    type: "geojson",
    data: { type: "FeatureCollection", features: [] },
    promoteId: "rid",
  });
  map.addLayer({
    id: "relatos-fill",
    type: "fill",
    source: "relatos",
    filter: ["==", ["geometry-type"], "Polygon"],
    paint: {
      "fill-color": KIND_COLOR,
      "fill-opacity": ["case", ["boolean", ["feature-state", "selected"], false], 0.45, 0.2],
    },
  });
  map.addLayer({
    id: "relatos-line",
    type: "line",
    source: "relatos",
    filter: ["==", ["geometry-type"], "Polygon"],
    paint: {
      "line-color": KIND_COLOR,
      "line-width": ["case", ["==", ["get", "kind"], "emergency"], 3, 2],
    },
  });
  map.addLayer({
    id: "relatos-pin",
    type: "circle",
    source: "relatos",
    filter: ["==", ["geometry-type"], "Point"],
    paint: {
      "circle-radius": 8,
      "circle-color": KIND_COLOR,
      "circle-stroke-color": "#ffffff",
      "circle-stroke-width": 2,
    },
  });
}
