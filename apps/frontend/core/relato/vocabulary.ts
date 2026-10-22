import type { RelatoKind, Species } from "../api/client";

// One vocabulary for web and a future native app: labels, help text, map colors.

export interface KindInfo {
  label: string;
  help: string;
  color: string;
}

export const KINDS: Record<RelatoKind, KindInfo> = {
  emergency: {
    label: "Emergência",
    help: "Ferido, preso, atropelado ou em perigo agora",
    color: "#D62828",
  },
  lost: { label: "Perdi meu animal", help: "Ele sumiu e eu estou procurando", color: "#7B2CBF" },
  found: {
    label: "Encontrei um animal",
    help: "Está comigo ou parado num lugar e parece ter dono",
    color: "#2A9D8F",
  },
  sighting: { label: "Vi um animal na rua", help: "Só quero registrar onde ele estava", color: "#1D4ED8" },
};

export const KIND_ORDER: RelatoKind[] = ["emergency", "lost", "found", "sighting"];

export const SPECIES: Record<Species, string> = { dog: "Cão", cat: "Gato", other: "Outro" };

export const SIZES = { small: "Pequeno", medium: "Médio", large: "Grande" } as const;

export const COAT_COLORS = {
  black: "Preto",
  white: "Branco",
  caramel: "Caramelo",
  brown: "Marrom",
  gray: "Cinza",
  tabby: "Rajado",
  tricolor: "Tricolor",
  spotted: "Malhado",
} as const;

export type Size = keyof typeof SIZES;
export type CoatColor = keyof typeof COAT_COLORS;

export function kindTitle(kind: RelatoKind, species: Species): string {
  const animal = species === "cat" ? "Gato" : species === "dog" ? "Cão" : "Animal";
  switch (kind) {
    case "emergency":
      return `${animal} em emergência`;
    case "lost":
      return `${animal} perdido`;
    case "found":
      return `${animal} encontrado`;
    case "sighting":
      return `${animal} visto na rua`;
  }
}
