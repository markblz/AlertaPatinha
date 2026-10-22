import { MapView } from "@/features/map/MapView";
import { PrecisionLegend } from "@/features/map/PrecisionLegend";

const DEV_STYLE_URL = "https://tiles.openfreemap.org/styles/liberty";

export default function HomePage() {
  const styleUrl = process.env.NEXT_PUBLIC_MAP_STYLE_URL || DEV_STYLE_URL;

  return (
    <main className="relative h-dvh w-full">
      <MapView styleUrl={styleUrl} />
      <header className="pointer-events-none absolute left-4 top-4 rounded-xl bg-white/95 px-4 py-2 shadow-lg">
        <h1 className="text-lg font-bold text-neutral-900">Alerta Patinha</h1>
      </header>
      <PrecisionLegend />
    </main>
  );
}
