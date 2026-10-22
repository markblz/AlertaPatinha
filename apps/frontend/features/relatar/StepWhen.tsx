"use client";

import { useMemo, useState } from "react";

import { seenOptions } from "@/core/relato/seen";
import { COAT_COLORS, type CoatColor, SIZES, type Size } from "@/core/relato/vocabulary";
import type { Draft, Flag } from "@/features/relatar/draft";
import { Chip } from "@/features/relatar/ui";

const FLAGS: { value: Flag; label: string }[] = [
  { value: "community", label: "É comunitário (a vizinhança cuida)" },
  { value: "colony", label: "Faz parte de uma colônia de gatos" },
  { value: "sensitive", label: "É de raça e pode ser furtado" },
];

function toggle<T>(list: T[], value: T): T[] {
  return list.includes(value) ? list.filter((v) => v !== value) : [...list, value];
}

export function StepWhen({
  draft,
  update,
  error,
}: {
  draft: Draft;
  update: (patch: Partial<Draft>) => void;
  error: string | null;
}) {
  const options = useMemo(() => seenOptions(new Date()), []);
  const isPreset = options.some((o) => draft.seen && o.text === draft.seen.text);
  const [other, setOther] = useState(draft.seen && !isPreset ? (draft.seen.text ?? "") : "");
  const otherActive = draft.seen !== undefined && !isPreset;

  return (
    <div className="space-y-6">
      <div role="radiogroup" aria-label="Quando você viu" className="flex flex-wrap gap-2">
        {options.map((o) => (
          <Chip
            key={o.label}
            selected={draft.seen !== undefined && draft.seen.text === o.text}
            onClick={() => update({ seen: { text: o.text } })}
          >
            {o.label}
          </Chip>
        ))}
      </div>

      <label className="block">
        <span className="mb-1 block font-semibold">Outro horário</span>
        <input
          type="text"
          inputMode="text"
          enterKeyHint="done"
          maxLength={120}
          value={other}
          placeholder="Ex.: anteontem à noite"
          onChange={(e) => {
            setOther(e.target.value);
            update({ seen: e.target.value.trim() ? { text: e.target.value.trim() } : undefined });
          }}
          className={`h-12 w-full rounded-lg border-2 px-3 text-base ${
            otherActive ? "border-tinta" : "border-nevoa"
          }`}
        />
      </label>
      {error && (
        <p role="alert" className="rounded-lg border-2 border-emergencia px-3 py-2 text-[0.9375rem]">
          {error}
        </p>
      )}

      <details className="rounded-xl border-2 border-nevoa p-3 [&_summary]:list-none">
        <summary className="flex min-h-8 cursor-pointer items-center justify-between font-semibold">
          Detalhes do animal (opcional)
          <span aria-hidden="true">＋</span>
        </summary>
        <div className="mt-4 space-y-5">
          <fieldset>
            <legend className="mb-2 font-semibold">Tamanho</legend>
            <div role="radiogroup" className="flex flex-wrap gap-2">
              {(Object.keys(SIZES) as Size[]).map((s) => (
                <Chip key={s} selected={draft.size === s} onClick={() => update({ size: draft.size === s ? undefined : s })}>
                  {SIZES[s]}
                </Chip>
              ))}
            </div>
          </fieldset>
          <fieldset>
            <legend className="mb-2 font-semibold">Cor (até 3)</legend>
            <div className="flex flex-wrap gap-2">
              {(Object.keys(COAT_COLORS) as CoatColor[]).map((c) => (
                <Chip
                  key={c}
                  role="checkbox"
                  selected={draft.colors.includes(c)}
                  onClick={() =>
                    (draft.colors.includes(c) || draft.colors.length < 3) &&
                    update({ colors: toggle(draft.colors, c) })
                  }
                >
                  {COAT_COLORS[c]}
                </Chip>
              ))}
            </div>
          </fieldset>
          <fieldset className="flex flex-wrap gap-2">
            <legend className="mb-2 font-semibold">Como ele está</legend>
            <Chip role="checkbox" selected={draft.injured === true} onClick={() => update({ injured: draft.injured ? undefined : true })}>
              Parece ferido
            </Chip>
            <Chip role="checkbox" selected={draft.collar === true} onClick={() => update({ collar: draft.collar ? undefined : true })}>
              Tem coleira
            </Chip>
          </fieldset>
          <fieldset className="space-y-2">
            <legend className="mb-2 font-semibold">Proteção do local</legend>
            {FLAGS.map((f) => (
              <label key={f.value} className="flex min-h-11 items-center gap-3">
                <input
                  type="checkbox"
                  className="h-5 w-5 accent-tinta"
                  checked={draft.flags.includes(f.value)}
                  onChange={() => update({ flags: toggle(draft.flags, f.value) })}
                />
                {f.label}
              </label>
            ))}
            <p className="text-sm text-tinta-suave">Marcando, mostramos uma área maior no mapa.</p>
          </fieldset>
        </div>
      </details>
    </div>
  );
}
