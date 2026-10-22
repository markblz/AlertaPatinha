"use client";

import type { ReactNode } from "react";

const STEPS = 3;

export function StepFrame({
  step,
  title,
  onBack,
  children,
  action,
}: {
  step: number;
  title: string;
  onBack: () => void;
  children: ReactNode;
  action: ReactNode;
}) {
  return (
    <main className="flex h-dvh flex-col bg-papel">
      <header className="shrink-0 px-4 pt-[calc(0.5rem+var(--spacing-safe-t))]">
        <div className="flex h-12 items-center gap-2">
          <button
            type="button"
            onClick={onBack}
            aria-label={step === 1 ? "Cancelar e voltar ao mapa" : "Voltar"}
            className="-ml-2 grid h-11 w-11 place-items-center rounded-full text-2xl"
          >
            ‹
          </button>
          <span className="text-sm font-semibold text-tinta-suave">
            {step} de {STEPS}
          </span>
        </div>
        <div className="flex gap-1.5" aria-hidden="true">
          {Array.from({ length: STEPS }, (_, i) => (
            <span key={i} className={`h-1.5 flex-1 rounded-full ${i < step ? "bg-tinta" : "bg-nevoa"}`} />
          ))}
        </div>
        <h1 className="mt-4 font-display text-[2rem] leading-[1.05]">{title}</h1>
      </header>
      <div className="min-h-0 flex-1 overflow-y-auto px-4 pb-4 pt-3">{children}</div>
      <footer className="shrink-0 border-t border-nevoa px-4 pb-[calc(0.75rem+var(--spacing-safe-b))] pt-3">
        {action}
      </footer>
    </main>
  );
}

export function PrimaryButton({
  children,
  disabled,
  onClick,
  tone = "ink",
}: {
  children: ReactNode;
  disabled?: boolean;
  onClick: () => void;
  tone?: "ink" | "sign";
}) {
  const look =
    tone === "sign"
      ? "border-[3px] border-tinta bg-sinal text-tinta shadow-[0_3px_0_var(--color-tinta)] active:translate-y-0.5 active:shadow-none"
      : "bg-tinta text-papel";
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={onClick}
      className={`flex h-14 w-full items-center justify-center rounded-xl font-display text-[1.5rem] disabled:opacity-35 ${look}`}
    >
      {children}
    </button>
  );
}

export function Chip({
  selected,
  onClick,
  children,
  role = "radio",
}: {
  selected: boolean;
  onClick: () => void;
  children: ReactNode;
  role?: "radio" | "checkbox";
}) {
  return (
    <button
      type="button"
      role={role}
      aria-checked={selected}
      onClick={onClick}
      className={`min-h-11 rounded-full border-2 px-4 text-[0.9375rem] font-semibold ${
        selected ? "border-tinta bg-tinta text-papel" : "border-nevoa bg-papel text-tinta"
      }`}
    >
      {children}
    </button>
  );
}
