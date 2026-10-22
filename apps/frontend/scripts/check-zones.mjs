// Two zones (docs/adr/0011-mobile-first-native-ready.md):
//   public  app/(public)/**  server-rendered share pages (Open Graph for WhatsApp)
//   app     app/(app)/**     screens that must survive `output: "export"` inside a
//                            Capacitor shell, plus everything they use:
//                            features/ platform/ core/
// The app zone may not use anything a static export rejects.
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname;
const APP_ZONE = ["app/(app)", "features", "platform", "core"];
const FORBIDDEN = [
  [/["']use server["']/, "Server Actions (writes go through the FastAPI API)"],
  [/from\s+["']next\/headers["']/, "next/headers (cookies/headers need a server)"],
  [/from\s+["']next\/server["']/, "next/server"],
  [/from\s+["']@\/server\//, "@/server (public zone only)"],
  [/export\s+(async\s+)?function\s+generateStaticParams/, "generateStaticParams (no dynamic routes in the app zone)"],
  [/export\s+const\s+(dynamic|revalidate)\s*=/, "route segment config"],
];

function* walk(dir) {
  for (const name of readdirSync(dir)) {
    const path = join(dir, name);
    if (statSync(path).isDirectory()) {
      if (dir.includes("app/(app)") && name.startsWith("[")) yield { path, dynamic: true };
      yield* walk(path);
    } else if (/\.(ts|tsx|mjs)$/.test(name) && !name.endsWith(".d.ts")) yield { path };
  }
}

const problems = [];
for (const zoneDir of APP_ZONE) {
  for (const { path, dynamic } of walk(join(ROOT, zoneDir))) {
    const rel = relative(ROOT, path);
    if (dynamic) problems.push(`${rel}: dynamic route segment (use a query param in the app zone)`);
    else if (/\/route\.(ts|tsx)$/.test(rel) && rel.startsWith("app/")) problems.push(`${rel}: route handler`);
    else {
      const source = readFileSync(path, "utf8");
      for (const [pattern, why] of FORBIDDEN) if (pattern.test(source)) problems.push(`${rel}: ${why}`);
    }
  }
}

if (problems.length) {
  console.error("App zone must stay static-exportable:\n  " + problems.join("\n  "));
  process.exit(1);
}
console.log("app zone is static-exportable");
