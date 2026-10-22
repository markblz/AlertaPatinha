import type { CreateRelatoBody, RelatoKind, Species } from "@/core/api/client";
import type { CoatColor, Size } from "@/core/relato/vocabulary";

export type Flag = "community" | "colony" | "sensitive";

export interface Place {
  lat: number;
  lng: number;
  accuracyM: number | null;
  source: "gps" | "pin";
}

export interface Draft {
  clientId: string; // fixed for the whole flow: retries must reuse it
  kind?: RelatoKind;
  species?: Species;
  count: number;
  place?: Place;
  seen?: { text: string | null }; // undefined = not chosen yet; text null = "agora"
  size?: Size;
  colors: CoatColor[];
  collar?: boolean;
  injured?: boolean;
  flags: Flag[];
}

export function newDraft(clientId: string): Draft {
  return { clientId, count: 1, colors: [], flags: [] };
}

export function toBody(d: Draft): CreateRelatoBody {
  if (!d.kind || !d.species || !d.place || !d.seen) throw new Error("incomplete draft");
  return {
    client_id: d.clientId,
    kind: d.kind,
    species: d.species,
    animal_count: d.count,
    location: {
      lat: d.place.lat,
      lng: d.place.lng,
      accuracy_m: d.place.accuracyM,
      source: d.place.source,
    },
    seen_text: d.seen.text,
    flags: d.flags,
    attributes: {
      size: d.size ?? null,
      coat_colors: d.colors,
      collar: d.collar ?? null,
      injured: d.injured ?? null,
    },
  };
}
