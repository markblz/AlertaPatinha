"use client";

import "maplibre-gl/dist/maplibre-gl.css";

import { GeolocateControl, Map as MapLibreMap, NavigationControl } from "maplibre-gl";
import { useEffect, useRef } from "react";

const BRAZIL_CENTER: [number, number] = [-51.9, -14.2];

export function MapView({ styleUrl }: { styleUrl: string }) {
  const container = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!container.current) return;
    const map = new MapLibreMap({
      container: container.current,
      style: styleUrl,
      center: BRAZIL_CENTER,
      zoom: 3.5,
      attributionControl: { compact: true },
    });
    map.addControl(new NavigationControl({ showCompass: false }), "top-right");
    map.addControl(
      new GeolocateControl({ positionOptions: { enableHighAccuracy: true } }),
      "top-right",
    );
    return () => map.remove();
  }, [styleUrl]);

  return <div ref={container} className="h-full w-full" />;
}
