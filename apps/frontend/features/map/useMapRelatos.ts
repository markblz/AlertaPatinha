"use client";

import type { GeoJSONSource, Map as MapLibreMap } from "maplibre-gl";
import { useEffect, useState } from "react";

import type { MapFeature } from "@/core/api/client";
import { api } from "@/platform/web/api";

export type TimeWindow = "24h" | "7d" | "30d";
const WINDOW_MS: Record<TimeWindow, number> = { "24h": 86_400_000, "7d": 7 * 86_400_000, "30d": 30 * 86_400_000 };

export type MapStatus = "idle" | "loading" | "zoom_in" | "truncated" | "offline";

/** Keeps the "relatos" source in sync with the visible area and time window. */
export function useMapRelatos(map: MapLibreMap | null, timeWindow: TimeWindow) {
  const [status, setStatus] = useState<MapStatus>("idle");
  const [features, setFeatures] = useState<MapFeature[]>([]);

  useEffect(() => {
    if (!map) return;
    let controller: AbortController | null = null;
    let timer: ReturnType<typeof setTimeout> | undefined;

    const load = async () => {
      controller?.abort();
      controller = new AbortController();
      const b = map.getBounds();
      const bbox = [b.getWest(), b.getSouth(), b.getEast(), b.getNorth()].map((n) => n.toFixed(5)).join(",");
      setStatus("loading");
      try {
        const { data } = await api.GET("/api/v1/map", {
          params: { query: { bbox, since: new Date(Date.now() - WINDOW_MS[timeWindow]).toISOString() } },
          signal: controller.signal,
        });
        if (!data) return setStatus("idle");
        const source = map.getSource<GeoJSONSource>("relatos");
        source?.setData({
          type: "FeatureCollection",
          features: data.features.map((f) => ({
            type: "Feature",
            geometry: f.geometry,
            properties: { ...f.properties, rid: f.id },
          })),
        });
        setFeatures(data.features);
        setStatus(data.zoom_in ? "zoom_in" : data.truncated ? "truncated" : "idle");
      } catch (err) {
        if ((err as Error).name !== "AbortError") setStatus("offline");
      }
    };

    const schedule = () => {
      clearTimeout(timer);
      timer = setTimeout(load, 250);
    };
    map.on("moveend", schedule);
    load();
    return () => {
      map.off("moveend", schedule);
      clearTimeout(timer);
      controller?.abort();
    };
  }, [map, timeWindow]);

  return { status, features };
}
