import { cache } from "react";

import { createApiClient, type RelatoOut } from "@/core/api/client";

// Public zone only (server-rendered share pages). Calls the backend directly
// and forwards NO cookies: link previews and SSR always get public precision.
const backend = createApiClient({ baseUrl: process.env.BACKEND_INTERNAL_URL ?? "http://backend:8000" });

/** Deduplicated per request: generateMetadata, the page and the OG image share one fetch. */
export const publicRelato = cache(async (id: string): Promise<RelatoOut | null> => {
  if (!/^[0-9a-f-]{36}$/i.test(id)) return null;
  const { data } = await backend.GET("/api/v1/relatos/{relato_id}", {
    params: { path: { relato_id: id } },
    cache: "no-store",
  });
  return data ?? null;
});
