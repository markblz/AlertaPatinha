"use client";

import type { Map as MapLibreMap } from "maplibre-gl";
import { useEffect, useRef, useState } from "react";

import { BRAZIL_CENTER, loadMap } from "@/features/map/loadMap";
import type { Draft } from "@/features/relatar/draft";
import { currentPosition, type FixError } from "@/platform/web/device";

// Below this zoom a dropped pin is a guess at the neighbourhood, not a street.
export const MIN_PIN_ZOOM = 15;
// A GPS fix this good is enough on its own: the map is optional, not a gate.
export const GOOD_GPS_M = 100;

type Gps = "searching" | "found" | FixError;

const GPS_TEXT: Record<Gps, string> = {
  searching: "Procurando sua localização…",
  found: "Arraste o mapa se o pino não estiver no lugar certo.",
  denied: "Sem acesso à localização. Arraste o mapa até onde o animal está.",
  unavailable: "Não conseguimos sua localização. Arraste o mapa até o local.",
  timeout: "A localização demorou. Arraste o mapa até o local.",
};

export function placeIsUsable(draft: Draft, zoom: number): boolean {
  const p = draft.place;
  if (!p) return false;
  if (p.source === "gps" && p.accuracyM !== null && p.accuracyM <= GOOD_GPS_M) return true;
  return zoom >= MIN_PIN_ZOOM;
}

export function StepPlace({
  draft,
  update,
  onZoomChange,
}: {
  draft: Draft;
  update: (patch: Partial<Draft>) => void;
  onZoomChange: (zoom: number) => void;
}) {
  const container = useRef<HTMLDivElement>(null);
  const mapRef = useRef<MapLibreMap | null>(null);
  const userMoved = useRef(false);
  const placeRef = useRef(draft.place);
  placeRef.current = draft.place;
  const [gps, setGps] = useState<Gps>(draft.place ? "found" : "searching");
  const [accuracy, setAccuracy] = useState<number | null>(draft.place?.accuracyM ?? null);

  // GPS and the map load in parallel. On a slow phone the fix often arrives
  // first, and the step can be completed even if the map never loads.
  useEffect(() => {
    if (draft.place) return;
    let cancelled = false;
    currentPosition()
      .then((fix) => {
        if (cancelled || userMoved.current) return;
        setGps("found");
        setAccuracy(fix.accuracyM);
        update({ place: { lat: fix.lat, lng: fix.lng, accuracyM: fix.accuracyM, source: "gps" } });
        mapRef.current?.jumpTo({ center: [fix.lng, fix.lat], zoom: 17 });
      })
      .catch((err: FixError) => !cancelled && setGps(err));
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const abort = new AbortController();
    const start = draft.place;
    loadMap(
      {
        container: container.current!,
        center: start ? [start.lng, start.lat] : BRAZIL_CENTER,
        zoom: start ? 17 : 3.5,
      },
      abort.signal,
    ).then((m) => {
      if (!m) return;
      mapRef.current = m;
      const fix = placeRef.current;
      if (fix?.source === "gps" && !userMoved.current) m.jumpTo({ center: [fix.lng, fix.lat], zoom: 17 });
      onZoomChange(m.getZoom());
      m.on("dragstart", () => {
        userMoved.current = true;
      });
      m.on("moveend", () => {
        onZoomChange(m.getZoom());
        if (!userMoved.current) return;
        const c = m.getCenter();
        setAccuracy(null);
        update({ place: { lat: c.lat, lng: c.lng, accuracyM: null, source: "pin" } });
      });
    });
    return () => {
      abort.abort();
      mapRef.current?.remove();
      mapRef.current = null;
    };
    // Mount once: the map owns its viewport from here on.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // A fix that landed before the map finished loading.
  useEffect(() => {
    const p = draft.place;
    const m = mapRef.current;
    if (m && p && p.source === "gps" && !userMoved.current) {
      m.jumpTo({ center: [p.lng, p.lat], zoom: 17 });
    }
  }, [draft.place]);

  return (
    <div className="flex h-full flex-col gap-3">
      <div className="relative min-h-64 flex-1 overflow-hidden rounded-xl border-2 border-nevoa bg-nevoa">
        <div className="absolute inset-0">
          <div ref={container} className="h-full w-full" />
        </div>
        {/* The map moves under a fixed pin: easier with a thumb than dragging a marker. */}
        <svg
          width="40"
          height="52"
          viewBox="0 0 40 52"
          aria-hidden="true"
          className="pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-full drop-shadow-md"
        >
          <path d="M20 50s17-15 17-30A17 17 0 0 0 3 20c0 15 17 30 17 30z" fill="#1b1f3b" stroke="#ffce00" strokeWidth="3" />
          <circle cx="20" cy="20" r="6" fill="#ffce00" />
        </svg>
      </div>
      <p className="text-[0.9375rem] text-tinta-suave" role="status">
        {GPS_TEXT[gps]}
        {accuracy !== null && ` Precisão do GPS: ±${accuracy} m.`}
      </p>
      <p className="rounded-lg bg-nevoa px-3 py-2 text-sm text-tinta-suave">
        No mapa público aparece só a área aproximada. O ponto exato fica protegido.
      </p>
    </div>
  );
}
