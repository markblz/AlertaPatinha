"use client";

import type { Species } from "@/core/api/client";
import { KIND_ORDER, KINDS, SPECIES } from "@/core/relato/vocabulary";
import type { Draft } from "@/features/relatar/draft";
import { Chip } from "@/features/relatar/ui";

export function StepKind({ draft, update }: { draft: Draft; update: (patch: Partial<Draft>) => void }) {
  return (
    <div className="space-y-6">
      <div role="radiogroup" aria-label="O que está acontecendo" className="space-y-2">
        {KIND_ORDER.map((kind) => {
          const info = KINDS[kind];
          const selected = draft.kind === kind;
          return (
            <button
              key={kind}
              type="button"
              role="radio"
              aria-checked={selected}
              onClick={() => update({ kind })}
              className={`flex w-full items-stretch gap-3 rounded-xl border-2 p-3 text-left ${
                selected ? "border-tinta bg-nevoa" : "border-nevoa"
              }`}
            >
              <span className="w-1.5 shrink-0 rounded-full" style={{ background: info.color }} />
              <span>
                <span className="block text-lg font-semibold leading-snug">{info.label}</span>
                <span className="block text-[0.9375rem] text-tinta-suave">{info.help}</span>
              </span>
            </button>
          );
        })}
      </div>

      <fieldset>
        <legend className="mb-2 text-lg font-semibold">Qual animal?</legend>
        <div role="radiogroup" className="flex flex-wrap gap-2">
          {(Object.keys(SPECIES) as Species[]).map((s) => (
            <Chip key={s} selected={draft.species === s} onClick={() => update({ species: s })}>
              {SPECIES[s]}
            </Chip>
          ))}
        </div>
      </fieldset>

      <fieldset>
        <legend className="mb-2 text-lg font-semibold">Quantos?</legend>
        <div className="flex items-center gap-4">
          <button
            type="button"
            aria-label="Menos um"
            disabled={draft.count <= 1}
            onClick={() => update({ count: draft.count - 1 })}
            className="grid h-11 w-11 place-items-center rounded-full border-2 border-tinta text-2xl disabled:opacity-30"
          >
            −
          </button>
          <output className="min-w-8 text-center font-display text-3xl" aria-live="polite">
            {draft.count}
          </output>
          <button
            type="button"
            aria-label="Mais um"
            disabled={draft.count >= 50}
            onClick={() => update({ count: draft.count + 1 })}
            className="grid h-11 w-11 place-items-center rounded-full border-2 border-tinta text-2xl disabled:opacity-30"
          >
            +
          </button>
        </div>
      </fieldset>
    </div>
  );
}
