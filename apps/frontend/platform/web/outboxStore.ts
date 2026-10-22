import { type IDBPDatabase, openDB } from "idb";

import type { OutboxItem, OutboxStore } from "@/core/outbox/outbox";

const DB_NAME = "alertapatinha";
const STORE = "outbox";

let db: Promise<IDBPDatabase> | null = null;

function open(): Promise<IDBPDatabase> {
  db ??= openDB(DB_NAME, 1, {
    upgrade(database) {
      database.createObjectStore(STORE, { keyPath: "id" });
    },
  });
  return db;
}

export const webOutboxStore: OutboxStore = {
  async put(item: OutboxItem) {
    await (await open()).put(STORE, item);
  },
  async delete(id: string) {
    await (await open()).delete(STORE, id);
  },
  async all() {
    return (await (await open()).getAll(STORE)) as OutboxItem[];
  },
};
