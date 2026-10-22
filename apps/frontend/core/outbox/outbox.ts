import type { CreateRelatoBody } from "../api/client";

// Offline-first writes. A relato is saved locally BEFORE the network is tried;
// the server is idempotent on client_id, so retrying is always safe.
// Storage is injected: IndexedDB on the web, SQLite/MMKV in a native app.

export interface OutboxItem {
  id: string; // = body.client_id
  body: CreateRelatoBody;
  createdAt: number;
  attempts: number;
  lastError?: string;
}

export interface OutboxStore {
  put(item: OutboxItem): Promise<void>;
  delete(id: string): Promise<void>;
  all(): Promise<OutboxItem[]>;
}

/** done = stored on the server · retry = keep for later · reject = the server will never accept it */
export type SendResult =
  | { status: "done"; relatoId: string }
  | { status: "retry"; error: string }
  | { status: "reject"; error: string };

export type Sender = (body: CreateRelatoBody) => Promise<SendResult>;

export interface FlushReport {
  sent: { item: OutboxItem; relatoId: string }[];
  rejected: { item: OutboxItem; error: string }[];
  pending: number;
}

export async function enqueue(store: OutboxStore, body: CreateRelatoBody, now: number): Promise<OutboxItem> {
  const item: OutboxItem = { id: body.client_id, body, createdAt: now, attempts: 0 };
  await store.put(item);
  return item;
}

/** Oldest first, one at a time: a flaky 3G link should not get N parallel uploads. */
export async function flush(store: OutboxStore, send: Sender): Promise<FlushReport> {
  const items = (await store.all()).sort((a, b) => a.createdAt - b.createdAt);
  const report: FlushReport = { sent: [], rejected: [], pending: 0 };
  for (const [index, item] of items.entries()) {
    const result = await send(item.body);
    if (result.status === "done") {
      await store.delete(item.id);
      report.sent.push({ item, relatoId: result.relatoId });
    } else if (result.status === "reject") {
      await store.delete(item.id);
      report.rejected.push({ item, error: result.error });
    } else {
      await store.put({ ...item, attempts: item.attempts + 1, lastError: result.error });
      // The network is the likely culprit: stop instead of burning data on the rest.
      report.pending = items.length - index;
      break;
    }
  }
  return report;
}
