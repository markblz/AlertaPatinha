import { ImageResponse } from "next/og";

// PWA/TWA icons from the brand mark: no binary assets to keep in sync.
// "maskable" keeps the sign inside Android's 80% safe zone on a yellow field.
const VARIANTS = {
  "192": { size: 192, padding: 0.06, background: "transparent" },
  "512": { size: 512, padding: 0.06, background: "transparent" },
  maskable: { size: 512, padding: 0.2, background: "#ffce00" },
} as const;

type Variant = keyof typeof VARIANTS;

export function generateImageMetadata() {
  return (Object.keys(VARIANTS) as Variant[]).map((id) => ({
    id,
    size: { width: VARIANTS[id].size, height: VARIANTS[id].size },
    contentType: "image/png",
  }));
}

export function signMark(size: number, padding: number, background: string) {
  const inner = Math.round(size * (1 - 2 * padding));
  return new ImageResponse(
    (
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", width: "100%", height: "100%", background }}>
        <svg width={inner} height={inner} viewBox="0 0 64 64">
          <rect x="10" y="10" width="44" height="44" rx="5" transform="rotate(45 32 32)" fill="#ffce00" stroke="#1b1f3b" strokeWidth="4" />
          <ellipse cx="32" cy="37" rx="7.5" ry="6.5" fill="#1b1f3b" />
          <ellipse cx="23.5" cy="28.5" rx="3" ry="3.8" fill="#1b1f3b" />
          <ellipse cx="29" cy="24" rx="3" ry="3.8" fill="#1b1f3b" />
          <ellipse cx="35" cy="24" rx="3" ry="3.8" fill="#1b1f3b" />
          <ellipse cx="40.5" cy="28.5" rx="3" ry="3.8" fill="#1b1f3b" />
        </svg>
      </div>
    ),
    { width: size, height: size },
  );
}

export default async function Icon({ id }: { id: Promise<string> }) {
  const v = VARIANTS[(await id) as Variant] ?? VARIANTS["192"];
  return signMark(v.size, v.padding, v.background);
}
