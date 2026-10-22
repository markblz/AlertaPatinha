"use client";

import type { Map as MapLibreMap, MapGeoJSONFeature } from "maplibre-gl";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";

import type { MapFeature } from "@/core/api/client";
import { PawSign, SignPlate } from "@/features/brand/SignPlate";
import { PrecisionLegend } from "@/features/map/PrecisionLegend";
import { RelatoSheet } from "@/features/map/RelatoSheet";
import { addRelatoLayers, BRAZIL_CENTER, loadMap } from "@/features/map/loadMap";
import { type MapStatus, type TimeWindow, useMapRelatos } from "@/features/map/useMapRelatos";
import { useOutboxFlush } from "@/features/relatar/useOutbox";

const VIEW_KEY = "ap:last-view";
const WINDOWS: { value: TimeWindow; label: string }[] = [
  { value: "24h", label: "24 h" },
  { value: "7d", label: "7 dias" },
  { value: "30d", label: "30 dias" },
];
const STATUS_TEXT: Partial<Record<MapStatus, string>> = {
  zoom_in: "Aproxime o mapa para ver os relatos",
  truncated: "Muitos relatos aqui. Aproxime para ver todos.",
  offline: "Sem conexão. O mapa volta a atualizar quando a internet voltar.",
};

function savedView(): { center: [number, number]; zoom: number } | null {
  try {
    const raw = localStorage.getItem(VIEW_KEY);
    return raw ? (JSON.parse(raw) as { center: [number, number]; zoom: number }) : null;
  } catch {
    return null;
  }
}

export function MapScreen() {
  const container = useRef<HTMLDivElement>(null);
  const [map, setMap] = useState<MapLibreMap | null>(null);
  const [timeWindow, setTimeWindow] = useState<TimeWindow>("7d");
  const [selected, setSelected] = useState<string | null>(null);
  const { status, features } = useMapRelatos(map, timeWindow);
  const pending = useOutboxFlush();

  useEffect(() => {
    const abort = new AbortController();
    let instance: MapLibreMap | null = null;
    const view = savedView();
    loadMap(
      { container: container.current!, center: view?.center ?? BRAZIL_CENTER, zoom: view?.zoom ?? 3.5 },
      abort.signal,
      "top-right",
    ).then(async (m) => {
      if (!m) return;
      instance = m;
      // Before any await: the style can finish loading while we wait.
      m.on("load", () => {
        addRelatoLayers(m);
        setMap(m);
      });
      const { GeolocateControl } = await import("maplibre-gl");
      m.addControl(
        new GeolocateControl({ positionOptions: { enableHighAccuracy: true }, fitBoundsOptions: { maxZoom: 15 } }),
        "top-right",
      );
      m.on("moveend", () => {
        try {
          const c = m.getCenter();
          localStorage.setItem(VIEW_KEY, JSON.stringify({ center: [c.lng, c.lat], zoom: m.getZoom() }));
        } catch {
          // private mode: the map just starts at Brazil next time
        }
      });
    });
    return () => {
      abort.abort();
      instance?.remove();
    };
  }, []);

  useEffect(() => {
    if (!map) return;
    const onClick = (e: { features?: MapGeoJSONFeature[] }) => {
      const rid = e.features?.[0]?.properties?.rid as string | undefined;
      setSelected(rid ?? null);
    };
    const layers = ["relatos-fill", "relatos-pin"];
    for (const layer of layers) map.on("click", layer, onClick);
    return () => {
      for (const layer of layers) map.off("click", layer, onClick);
    };
  }, [map]);

  useEffect(() => {
    if (!map || !selected) return;
    map.setFeatureState({ source: "relatos", id: selected }, { selected: true });
    return () => {
      if (map.getSource("relatos")) map.setFeatureState({ source: "relatos", id: selected }, { selected: false });
    };
  }, [map, selected]);

  const selectedFeature: MapFeature | undefined = features.find((f) => f.id === selected);
  const statusText = STATUS_TEXT[status];

  return (
    <main className="map-under-header relative h-dvh w-full overflow-hidden">
      {/* maplibre-gl.css sets position:relative on the container: position the wrapper instead. */}
      <div className="absolute inset-0">
        <div ref={container} className="h-full w-full" />
      </div>

      <header className="pointer-events-none absolute inset-x-0 top-0 flex items-start justify-between gap-2 px-4 pt-[calc(0.75rem+var(--spacing-safe-t))]">
        <div className="pointer-events-auto">
          <SignPlate />
        </div>
        <div
          role="radiogroup"
          aria-label="Período"
          className="pointer-events-auto flex shrink-0 whitespace-nowrap rounded-lg border-2 border-tinta bg-papel p-0.5 text-sm font-semibold"
        >
          {WINDOWS.map((w) => (
            <button
              key={w.value}
              type="button"
              role="radio"
              aria-checked={timeWindow === w.value}
              onClick={() => setTimeWindow(w.value)}
              className={`h-9 rounded-md px-2.5 ${timeWindow === w.value ? "bg-tinta text-papel" : "text-tinta"}`}
            >
              {w.label}
            </button>
          ))}
        </div>
      </header>

      {(statusText || pending > 0) && (
        <p
          role="status"
          className="absolute inset-x-4 top-[calc(4.25rem+var(--spacing-safe-t))] mx-auto w-fit max-w-full rounded-full bg-tinta px-4 py-2 text-center text-sm text-papel"
        >
          {pending > 0
            ? `${pending} relato${pending > 1 ? "s" : ""} guardado${pending > 1 ? "s" : ""} no celular. Enviaremos quando a internet voltar.`
            : statusText}
        </p>
      )}

      <div className="pointer-events-none absolute inset-x-0 bottom-0 flex flex-col gap-3">
        {selectedFeature ? (
          <RelatoSheet feature={selectedFeature} onClose={() => setSelected(null)} />
        ) : (
          <>
            <div className="pointer-events-auto px-4">
              <PrecisionLegend />
            </div>
            <div className="pointer-events-auto px-4 pb-[calc(1rem+var(--spacing-safe-b))]">
              <Link
                href="/relatar"
                className="flex h-16 items-center justify-center gap-3 rounded-xl border-[3px] border-tinta bg-sinal font-display text-[1.6rem] text-tinta shadow-[0_3px_0_var(--color-tinta)] active:translate-y-0.5 active:bg-sinal-press active:shadow-none"
              >
                <PawSign size={34} />
                Relatar um animal
              </Link>
            </div>
          </>
        )}
      </div>
    </main>
  );
}
