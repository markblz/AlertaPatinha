import type { MetadataRoute } from "next";

// Installability matters beyond polish: iOS only delivers Web Push to
// home-screen-installed PWAs, and the Play Store TWA is built from this file.
export default function manifest(): MetadataRoute.Manifest {
  return {
    id: "/",
    name: "Alerta Patinha",
    short_name: "Alerta Patinha",
    description: "Relate e acompanhe animais perdidos, de rua e em emergência perto de você.",
    lang: "pt-BR",
    dir: "ltr",
    start_url: "/",
    scope: "/",
    display: "standalone",
    orientation: "portrait",
    background_color: "#ffffff",
    theme_color: "#ffce00",
    categories: ["social", "utilities"],
    icons: [
      { src: "/icon/192", sizes: "192x192", type: "image/png", purpose: "any" },
      { src: "/icon/512", sizes: "512x512", type: "image/png", purpose: "any" },
      { src: "/icon/maskable", sizes: "512x512", type: "image/png", purpose: "maskable" },
    ],
    shortcuts: [{ name: "Relatar um animal", short_name: "Relatar", url: "/relatar" }],
  };
}
