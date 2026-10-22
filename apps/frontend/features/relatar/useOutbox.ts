"use client";

import { useEffect, useState } from "react";

import type { CreateRelatoBody } from "@/core/api/client";
import { enqueue, flush } from "@/core/outbox/outbox";
import { relatoSender } from "@/core/outbox/relatoSender";
import { api, ensureWebSession } from "@/platform/web/api";
import { webOutboxStore } from "@/platform/web/outboxStore";

const send = relatoSender(api, ensureWebSession);

export type SubmitOutcome =
  | { status: "sent"; relatoId: string }
  | { status: "queued" }
  | { status: "rejected"; error: string };

/** Save first, then try the network: a relato typed on 3G is never lost. */
export async function submitRelato(body: CreateRelatoBody): Promise<SubmitOutcome> {
  await enqueue(webOutboxStore, body, Date.now());
  const report = await flush(webOutboxStore, send);
  const sent = report.sent.find((s) => s.item.id === body.client_id);
  if (sent) return { status: "sent", relatoId: sent.relatoId };
  const rejected = report.rejected.find((r) => r.item.id === body.client_id);
  if (rejected) return { status: "rejected", error: rejected.error };
  return { status: "queued" };
}

/** Sends anything left from earlier visits; returns how many are still waiting. */
export function useOutboxFlush(): number {
  const [pending, setPending] = useState(0);
  useEffect(() => {
    let alive = true;
    const run = async () => {
      try {
        const report = await flush(webOutboxStore, send);
        if (alive) setPending(report.pending);
      } catch {
        // IndexedDB unavailable (private mode on some browsers): nothing queued
      }
    };
    run();
    window.addEventListener("online", run);
    return () => {
      alive = false;
      window.removeEventListener("online", run);
    };
  }, []);
  return pending;
}
