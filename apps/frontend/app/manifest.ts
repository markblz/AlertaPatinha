import type { MetadataRoute } from "next";

// Installability matters beyond polish: iOS only delivers Web Push to
// home-screen-installed PWAs. Icons and the Serwist service worker land in M3.
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Alerta Patinha",
    short_name: "Alerta Patinha",
    description: "Relate e acompanhe animais perdidos, de rua e em emergência perto de você.",
    lang: "pt-BR",
    start_url: "/",
    display: "standalone",
    background_color: "#ffffff",
    theme_color: "#e8590c",
  };
}
