import type { Metadata, Viewport } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "Alerta Patinha",
  description: "Viu um animal precisando de ajuda? Relate, acompanhe e ajude perto de você.",
};

export const viewport: Viewport = {
  themeColor: "#e8590c",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
