// core/ must run unchanged in a future React Native app: no DOM, no Next, no React.
// Fails the build if anything platform-specific sneaks in.
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const ROOT = new URL("../core/", import.meta.url).pathname;
const ALLOWED_PACKAGES = new Set(["openapi-fetch"]);
const FORBIDDEN_GLOBALS =
  /\b(window|document|localStorage|sessionStorage|indexedDB|navigator|location)\s*[.[]/;

function* files(dir) {
  for (const name of readdirSync(dir)) {
    const path = join(dir, name);
    if (statSync(path).isDirectory()) yield* files(path);
    else if (/\.tsx?$/.test(name) && !name.endsWith(".d.ts")) yield path;
  }
}

const problems = [];
for (const file of files(ROOT)) {
  const source = readFileSync(file, "utf8");
  for (const [, spec] of source.matchAll(/from\s+["']([^"']+)["']/g)) {
    if (!spec.startsWith(".") && !ALLOWED_PACKAGES.has(spec)) {
      problems.push(`${file}: imports "${spec}"`);
    }
  }
  const global = source.match(FORBIDDEN_GLOBALS);
  if (global) problems.push(`${file}: uses browser global "${global[1]}"`);
  if (file.endsWith(".tsx")) problems.push(`${file}: JSX belongs in features/, not core/`);
}

if (problems.length) {
  console.error("core/ must stay platform-agnostic:\n  " + problems.join("\n  "));
  process.exit(1);
}
console.log("core/ is platform-agnostic");
