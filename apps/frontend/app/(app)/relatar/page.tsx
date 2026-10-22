import type { Metadata } from "next";

import { RelatarFlow } from "@/features/relatar/RelatarFlow";

export const metadata: Metadata = { title: "Relatar", robots: { index: false } };

export default function RelatarPage() {
  return <RelatarFlow />;
}
