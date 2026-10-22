import { createApiClient } from "@/core/api/client";

// Same origin: Next proxies /api/* to the backend and the session rides an
// HttpOnly cookie, so no token ever touches JavaScript on the web.
export const api = createApiClient({ baseUrl: "" });

export async function ensureWebSession(): Promise<void> {
  await api.POST("/api/v1/sessions/anonymous", { body: { delivery: "cookie" } });
}
