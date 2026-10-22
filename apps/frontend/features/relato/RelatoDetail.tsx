"use client";

import type { GeoJSONSource, Map as MapLibreMap } from "maplibre-gl";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";

import type { RelatoOut } from "@/core/api/client";
import { describeSeen } from "@/core/relato/seen";
import { COAT_COLORS, KINDS, kindTitle, SIZES } from "@/core/relato/vocabulary";
import { SignPlate } from "@/features/brand/SignPlate";
import { addRelatoLayers, loadMap } from "@/features/map/loadMap";
import { PrimaryButton } from "@/features/relatar/ui";
import { api } from "@/platform/web/api";
import { shareLink } from "@/platform/web/device";

function bounds(geometry: NonNullable<RelatoOut["location"]["geometry"]>): [[number, number], [number, number]] {
  const coords = geometry.type === "Point" ? [geometry.coordinates] : geometry.coordinates[0];
  const lngs = coords.map((c) => c[0]);
  const lats = coords.map((c) => c[1]);
  return [
    [Math.min(...lngs), Math.min(...lats)],
    [Math.max(...lngs), Math.max(...lats)],
  ];
}

function attributeChips(attrs: Record<string, unknown>): string[] {
  const chips: string[] = [];
  if (typeof attrs.size === "string" && attrs.size in SIZES) chips.push(SIZES[attrs.size as keyof typeof SIZES]);
  if (Array.isArray(attrs.coat_colors)) {
    for (const c of attrs.coat_colors) if (c in COAT_COLORS) chips.push(COAT_COLORS[c as keyof typeof COAT_COLORS]);
  }
  if (attrs.injured === true) chips.push("Parece ferido");
  if (attrs.collar === true) chips.push("Tem coleira");
  return chips;
}

export function RelatoDetail({ initial }: { initial: RelatoOut }) {
  const [relato, setRelato] = useState(initial);
  const container = useRef<HTMLDivElement>(null);
  const mapRef = useRef<MapLibreMap | null>(null);

  // The server rendered the public view; with the session cookie the reporter
  // gets their exact point (and the backend logs that read).
  useEffect(() => {
    api
      .GET("/api/v1/relatos/{relato_id}", { params: { path: { relato_id: initial.id } } })
      .then(({ data }) => data && setRelato(data))
      .catch(() => undefined);
  }, [initial.id]);

  const geometry = relato.location.geometry;
  const latest = useRef({ geometry, kind: relato.kind, id: relato.id });
  latest.current = { geometry, kind: relato.kind, id: relato.id };

  const apply = (m: MapLibreMap) => {
    const { geometry: g, kind, id } = latest.current;
    if (!g || !m.getSource("relatos")) return;
    m.getSource<GeoJSONSource>("relatos")?.setData({ type: "Feature", geometry: g, properties: { kind, rid: id } });
    m.fitBounds(bounds(g), { padding: 48, maxZoom: 16, duration: 0 });
  };

  // One map for the page's lifetime; data is applied on load and on change.
  useEffect(() => {
    const g = latest.current.geometry;
    if (!g || !container.current) return;
    const abort = new AbortController();
    loadMap({ container: container.current, bounds: bounds(g), fitBoundsOptions: { padding: 48, maxZoom: 16 } }, abort.signal)
      .then((m) => {
        if (!m) return;
        mapRef.current = m;
        m.on("load", () => {
          addRelatoLayers(m);
          apply(m);
        });
      })
      .catch(() => undefined);
    return () => {
      abort.abort();
      mapRef.current?.remove();
      mapRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Public view → exact point once the reporter's own fetch returns.
  useEffect(() => {
    if (mapRef.current?.isStyleLoaded()) apply(mapRef.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [geometry]);

  const kind = KINDS[relato.kind];
  const seen = describeSeen(relato.seen, new Date());
  const chips = attributeChips(relato.attributes);
  const share = () =>
    shareLink(
      kindTitle(relato.kind, relato.species),
      `${kindTitle(relato.kind, relato.species)}, visto ${seen}. Você pode ajudar?`,
      `${window.location.origin}/r/${relato.id}`,
    );

  return (
    <main className="mx-auto flex min-h-dvh max-w-xl flex-col bg-papel">
      <header className="flex items-center justify-between px-4 pb-3 pt-[calc(0.75rem+var(--spacing-safe-t))]">
        <Link href="/" aria-label="Ir para o mapa">
          <SignPlate />
        </Link>
      </header>

      <div ref={container} className="h-64 w-full bg-nevoa sm:rounded-xl" aria-label="Mapa do local" role="img" />

      <article className="flex-1 px-4 pt-5">
        <div className="flex items-start gap-3">
          <span className="mt-1 h-12 w-1.5 shrink-0 rounded-full" style={{ background: kind.color }} />
          <div>
            <h1 className="font-display text-[2.25rem] leading-[1.05]">{kindTitle(relato.kind, relato.species)}</h1>
            <p className="mt-1 text-lg text-tinta-suave">
              Visto {seen}
              {relato.animal_count > 1 && `, ${relato.animal_count} animais`}
            </p>
          </div>
        </div>

        {chips.length > 0 && (
          <ul className="mt-4 flex flex-wrap gap-2" aria-label="Detalhes do animal">
            {chips.map((c) => (
              <li key={c} className="rounded-full bg-nevoa px-3 py-1.5 text-[0.9375rem] font-semibold">
                {c}
              </li>
            ))}
          </ul>
        )}

        <p className="mt-5 rounded-lg bg-nevoa px-3 py-2 text-[0.9375rem] text-tinta-suave">
          {relato.location.mode === "exact"
            ? relato.is_mine
              ? "Você relatou isto. Só você vê o ponto exato; os outros veem uma área aproximada."
              : "Local exato."
            : relato.location.mode === "hidden"
              ? "Local protegido: este relato não aparece no mapa público."
              : "Local aproximado: o animal estava em algum ponto desta área. O ponto exato fica protegido."}
        </p>
      </article>

      <footer className="sticky bottom-0 space-y-2 bg-papel px-4 pb-[calc(1rem+var(--spacing-safe-b))] pt-3">
        <PrimaryButton tone="sign" onClick={share}>
          Compartilhar no WhatsApp
        </PrimaryButton>
        <Link href="/" className="flex h-12 items-center justify-center font-semibold underline underline-offset-4">
          Ver mapa
        </Link>
      </footer>
    </main>
  );
}
