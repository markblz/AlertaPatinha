import type { Metadata, Viewport } from "next";
import { Barlow, Barlow_Condensed } from "next/font/google";

import "./globals.css";

// Self-hosted at build time: no request to Google from the user's phone.
const barlow = Barlow({
  subsets: ["latin"],
  weight: ["400", "600"],
  variable: "--font-barlow",
  display: "swap",
});
const barlowCondensed = Barlow_Condensed({
  subsets: ["latin"],
  weight: ["700"],
  variable: "--font-barlow-condensed",
  display: "swap",
});

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3100";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: { default: "Alerta Patinha", template: "%s · Alerta Patinha" },
  description: "Viu um animal precisando de ajuda? Relate em segundos e acompanhe no mapa.",
  applicationName: "Alerta Patinha",
  appleWebApp: { capable: true, title: "Alerta Patinha", statusBarStyle: "default" },
  formatDetection: { telephone: false },
  openGraph: { siteName: "Alerta Patinha", locale: "pt_BR", type: "website" },
};

export const viewport: Viewport = {
  themeColor: "#ffce00",
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR" className={`${barlow.variable} ${barlowCondensed.variable}`}>
      <body>{children}</body>
    </html>
  );
}
