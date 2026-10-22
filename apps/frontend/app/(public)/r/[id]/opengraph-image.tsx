import { ImageResponse } from "next/og";

import { describeSeen } from "@/core/relato/seen";
import { KINDS, kindTitle } from "@/core/relato/vocabulary";
import { publicRelato } from "@/server/backend";

// WhatsApp: ≥300 px wide, ≤600 KB (aim < 300 KB), ≤ 4:1. Flat shapes keep this ~30 KB.
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";
export const alt = "Relato no Alerta Patinha";

export default async function OgImage({ params }: { params: Promise<{ id: string }> }) {
  const relato = await publicRelato((await params).id);
  const color = relato ? KINDS[relato.kind].color : "#4a4f6a";
  const title = relato ? kindTitle(relato.kind, relato.species) : "Relato não encontrado";
  const seen = relato ? `Visto ${describeSeen(relato.seen, new Date())}` : "";

  return new ImageResponse(
    (
      <div style={{ display: "flex", width: "100%", height: "100%", background: "#ffffff" }}>
        <div style={{ width: 28, background: color }} />
        <div style={{ display: "flex", flexDirection: "column", justifyContent: "space-between", padding: "64px 72px", flex: 1 }}>
          <div style={{ display: "flex", flexDirection: "column" }}>
            <div style={{ fontSize: 84, fontWeight: 700, color: "#1b1f3b", lineHeight: 1.05 }}>{title}</div>
            <div style={{ fontSize: 44, color: "#4a4f6a", marginTop: 24 }}>{seen}</div>
            <div style={{ fontSize: 34, color: "#4a4f6a", marginTop: 16 }}>
              Área aproximada no mapa. Você pode ajudar?
            </div>
          </div>
          <div style={{ display: "flex", alignItems: "center" }}>
            <div
              style={{
                display: "flex",
                background: "#ffce00",
                border: "6px solid #1b1f3b",
                borderRadius: 14,
                padding: "10px 28px",
                fontSize: 44,
                fontWeight: 700,
                color: "#1b1f3b",
              }}
            >
              Alerta Patinha
            </div>
          </div>
        </div>
      </div>
    ),
    size,
  );
}
