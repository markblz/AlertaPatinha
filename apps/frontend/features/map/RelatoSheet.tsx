"use client";

import Link from "next/link";

import type { MapFeature } from "@/core/api/client";
import { describeSeen } from "@/core/relato/seen";
import { KINDS, kindTitle } from "@/core/relato/vocabulary";

export function RelatoSheet({ feature, onClose }: { feature: MapFeature; onClose: () => void }) {
  const p = feature.properties;
  const kind = KINDS[p.kind];
  const seen = describeSeen({ start: p.seen_start, end: p.seen_end, precision: p.seen_precision }, new Date());
  const count = p.animal_count > 1 ? ` · ${p.animal_count} animais` : "";

  return (
    <section
      role="dialog"
      aria-label={kindTitle(p.kind, p.species)}
      className="pointer-events-auto rounded-t-2xl bg-papel px-4 pb-[calc(1rem+var(--spacing-safe-b))] pt-3 shadow-[0_-6px_24px_rgba(27,31,59,0.18)]"
    >
      <div className="mx-auto mb-3 h-1.5 w-10 rounded-full bg-nevoa" aria-hidden="true" />
      <div className="flex items-start gap-3">
        <span className="mt-1 h-10 w-1.5 shrink-0 rounded-full" style={{ background: kind.color }} />
        <div className="min-w-0 flex-1">
          <h2 className="font-display text-2xl leading-tight">{kindTitle(p.kind, p.species)}</h2>
          <p className="text-tinta-suave">
            Visto {seen}
            {count}
          </p>
        </div>
        <button
          type="button"
          onClick={onClose}
          className="-mr-2 -mt-1 grid h-11 w-11 place-items-center rounded-full text-2xl text-tinta-suave"
          aria-label="Fechar"
        >
          ×
        </button>
      </div>
      <p className="mt-3 rounded-lg bg-nevoa px-3 py-2 text-sm text-tinta-suave">
        {p.display_mode === "exact"
          ? "Local exato informado por quem relatou."
          : "Local aproximado: o animal estava em algum ponto desta área. O ponto exato fica protegido."}
      </p>
      <Link
        href={`/r/${feature.id}`}
        className="mt-3 flex h-12 items-center justify-center rounded-lg border-2 border-tinta font-display text-xl"
      >
        Ver relato
      </Link>
    </section>
  );
}
