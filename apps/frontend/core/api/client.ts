import createClient from "openapi-fetch";

import type { components, paths } from "./schema";

export type Schemas = components["schemas"];
export type CreateRelatoBody = Schemas["CreateRelatoIn"];
export type RelatoOut = Schemas["RelatoOut"];
export type MapOut = Schemas["MapOut"];
export type MapFeature = Schemas["MapFeatureOut"];
export type RelatoKind = Schemas["RelatoKind"];
export type Species = Schemas["Species"];
export type TimePrecision = Schemas["TimePrecision"];
export type ApiErrorBody = Schemas["ErrorBody"];

export interface ClientOptions {
  /** "" on the web (same origin, Next proxies /api); the site's full URL in a native app. */
  baseUrl: string;
  /** Native apps: return the stored session token (sent as Bearer). Web: omit (HttpOnly cookie). */
  getToken?: () => string | null | Promise<string | null>;
}

export function createApiClient({ baseUrl, getToken }: ClientOptions) {
  const client = createClient<paths>({ baseUrl, credentials: "same-origin" });
  if (getToken) {
    client.use({
      async onRequest({ request }) {
        const token = await getToken();
        if (token) request.headers.set("Authorization", `Bearer ${token}`);
        return request;
      },
    });
  }
  return client;
}

export type ApiClient = ReturnType<typeof createApiClient>;

export function errorCode(error: unknown): string | undefined {
  if (error && typeof error === "object" && "detail" in error) {
    const detail = (error as { detail?: { code?: unknown } }).detail;
    if (typeof detail?.code === "string") return detail.code;
  }
  return undefined;
}
