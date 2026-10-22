// Browser capabilities behind small functions, so a native shell swaps the
// implementation (Capacitor/Expo plugins) without touching features/.

export interface Fix {
  lat: number;
  lng: number;
  accuracyM: number;
}

export type FixError = "denied" | "unavailable" | "timeout";

export function currentPosition(timeoutMs = 15_000): Promise<Fix> {
  return new Promise((resolve, reject: (e: FixError) => void) => {
    if (!("geolocation" in navigator)) return reject("unavailable");
    navigator.geolocation.getCurrentPosition(
      (pos) =>
        resolve({
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
          accuracyM: Math.round(pos.coords.accuracy),
        }),
      (err) =>
        reject(err.code === err.PERMISSION_DENIED ? "denied" : err.code === err.TIMEOUT ? "timeout" : "unavailable"),
      { enableHighAccuracy: true, timeout: timeoutMs, maximumAge: 30_000 },
    );
  });
}

export function newClientId(): string {
  return crypto.randomUUID();
}

/** Native share sheet (WhatsApp is one tap away on Android/iOS); WhatsApp link as fallback. */
export async function shareLink(title: string, text: string, url: string): Promise<"shared" | "whatsapp"> {
  if (typeof navigator.share === "function") {
    try {
      await navigator.share({ title, text, url });
      return "shared";
    } catch {
      // cancelled or unsupported payload: fall through to WhatsApp
    }
  }
  window.open(`https://wa.me/?text=${encodeURIComponent(`${text} ${url}`)}`, "_blank", "noopener");
  return "whatsapp";
}
