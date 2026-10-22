"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { PawSign } from "@/features/brand/SignPlate";
import { type Draft, newDraft, toBody } from "@/features/relatar/draft";
import { StepKind } from "@/features/relatar/StepKind";
import { placeIsUsable, StepPlace } from "@/features/relatar/StepPlace";
import { StepWhen } from "@/features/relatar/StepWhen";
import { PrimaryButton, StepFrame } from "@/features/relatar/ui";
import { type SubmitOutcome, submitRelato } from "@/features/relatar/useOutbox";
import { ensureWebSession } from "@/platform/web/api";
import { newClientId, shareLink } from "@/platform/web/device";

const REJECTION_TEXT: Record<string, string> = {
  seen_unparseable: "Não entendemos esse horário. Escolha uma opção acima ou escreva como “ontem à noite”.",
  validation_error: "Faltou alguma informação. Confira os passos e tente de novo.",
};

export function RelatarFlow() {
  const router = useRouter();
  const [draft, setDraft] = useState<Draft>(() => newDraft(newClientId()));
  const [step, setStep] = useState(1);
  const [zoom, setZoom] = useState(0);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [outcome, setOutcome] = useState<SubmitOutcome | null>(null);
  const update = (patch: Partial<Draft>) => setDraft((d) => ({ ...d, ...patch }));

  const back = () => (step === 1 ? router.push("/") : setStep(step - 1));

  // Warm up while the user picks the kind: the session (so the first POST is
  // not a 401 round trip on 3G) and the map bundle (so step 2 opens fast).
  useEffect(() => {
    ensureWebSession().catch(() => undefined); // offline: the outbox retries later
    const idle = window.requestIdleCallback ?? ((cb: () => void) => setTimeout(cb, 1200));
    idle(() => void import("maplibre-gl"));
  }, []);

  const send = async () => {
    setSending(true);
    setError(null);
    const result = await submitRelato(toBody(draft));
    setSending(false);
    if (result.status === "rejected") {
      setError(REJECTION_TEXT[result.error] ?? "Não foi possível enviar. Confira os dados e tente de novo.");
      return;
    }
    setOutcome(result);
  };

  if (outcome) return <Done outcome={outcome} />;

  if (step === 1) {
    return (
      <StepFrame
        step={1}
        title="O que está acontecendo?"
        onBack={back}
        action={
          <PrimaryButton disabled={!draft.kind || !draft.species} onClick={() => setStep(2)}>
            Continuar
          </PrimaryButton>
        }
      >
        <StepKind draft={draft} update={update} />
      </StepFrame>
    );
  }

  if (step === 2) {
    const usable = placeIsUsable(draft, zoom);
    return (
      <StepFrame
        step={2}
        title="Onde ele está?"
        onBack={back}
        action={
          <PrimaryButton disabled={!usable} onClick={() => setStep(3)}>
            {draft.place && !usable ? "Aproxime o mapa até a rua" : "Confirmar local"}
          </PrimaryButton>
        }
      >
        <StepPlace draft={draft} update={update} onZoomChange={setZoom} />
      </StepFrame>
    );
  }

  return (
    <StepFrame
      step={3}
      title="Quando você viu?"
      onBack={back}
      action={
        <PrimaryButton tone="sign" disabled={!draft.seen || sending} onClick={send}>
          {sending ? "Enviando…" : "Enviar relato"}
        </PrimaryButton>
      }
    >
      <StepWhen draft={draft} update={update} error={error} />
    </StepFrame>
  );
}

function Done({ outcome }: { outcome: SubmitOutcome }) {
  const sent = outcome.status === "sent" ? outcome : null;
  const share = () => {
    if (!sent) return;
    const url = `${window.location.origin}/r/${sent.relatoId}`;
    shareLink("Alerta Patinha", "Vi um animal precisando de atenção. Você pode ajudar?", url);
  };

  return (
    <main className="flex h-dvh flex-col justify-between bg-papel px-4 pb-[calc(1rem+var(--spacing-safe-b))] pt-[calc(2rem+var(--spacing-safe-t))]">
      <div>
        <PawSign size={72} />
        <h1 className="mt-6 font-display text-[2.25rem] leading-[1.05]">
          {sent ? "Relato enviado" : "Relato guardado no celular"}
        </h1>
        <p className="mt-3 max-w-prose text-lg text-tinta-suave">
          {sent
            ? "Ele já aparece no mapa como uma área aproximada. Compartilhe para mais gente da região ver."
            : "Você está sem internet agora. Enviaremos sozinhos assim que a conexão voltar. Pode fechar o app."}
        </p>
      </div>
      <div className="space-y-3">
        {sent && (
          <PrimaryButton tone="sign" onClick={share}>
            Compartilhar no WhatsApp
          </PrimaryButton>
        )}
        {sent && (
          <Link
            href={`/r/${sent.relatoId}`}
            className="flex h-14 items-center justify-center rounded-xl border-2 border-tinta font-display text-[1.5rem]"
          >
            Ver relato
          </Link>
        )}
        <Link href="/" className="flex h-12 items-center justify-center font-semibold underline underline-offset-4">
          Voltar ao mapa
        </Link>
      </div>
    </main>
  );
}
