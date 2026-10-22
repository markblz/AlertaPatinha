// MapLibre 6 starts its worker from a file next to its own module; bundlers
// don't emit that file. Serve it from public/ (versioned for cache busting)
// and point setWorkerUrl at it (features/map/loadMap.ts).
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";

const pkg = JSON.parse(readFileSync(new URL("../node_modules/maplibre-gl/package.json", import.meta.url)));
const outDir = new URL("../public/maplibre/", import.meta.url);
mkdirSync(outDir, { recursive: true });
copyFileSync(
  new URL("../node_modules/maplibre-gl/dist/maplibre-gl-worker.mjs", import.meta.url),
  new URL(`maplibre-gl-worker.${pkg.version}.mjs`, outDir),
);
console.log(`maplibre worker ${pkg.version} → public/maplibre/`);
