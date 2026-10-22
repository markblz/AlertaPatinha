import { type ApiClient, errorCode } from "../api/client";
import type { Sender } from "./outbox";

/**
 * `ensureSession` differs per platform: the web asks for a cookie; a native
 * app asks for a token (delivery: "token") and keeps it in secure storage.
 */
export function relatoSender(api: ApiClient, ensureSession: () => Promise<void>): Sender {
  return async (body) => {
    try {
      let result = await api.POST("/api/v1/relatos", { body });
      if (result.response.status === 401) {
        await ensureSession();
        result = await api.POST("/api/v1/relatos", { body });
      }
      if (result.data) return { status: "done", relatoId: result.data.id };
      const status = result.response.status;
      const code = errorCode(result.error) ?? `http_${status}`;
      // 4xx (except timeouts/rate limits) will fail the same way forever.
      if (status >= 400 && status < 500 && status !== 408 && status !== 429) {
        return { status: "reject", error: code };
      }
      return { status: "retry", error: code };
    } catch {
      return { status: "retry", error: "network" };
    }
  };
}
