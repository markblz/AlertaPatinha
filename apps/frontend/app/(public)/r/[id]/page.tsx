import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { describeSeen } from "@/core/relato/seen";
import { kindTitle } from "@/core/relato/vocabulary";
import { RelatoDetail } from "@/features/relato/RelatoDetail";
import { publicRelato } from "@/server/backend";

// Public zone: server-rendered so WhatsApp/Telegram crawlers (which run no JS)
// get the title, description and preview image in the first bytes of <head>.

type Props = { params: Promise<{ id: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const relato = await publicRelato((await params).id);
  if (!relato) return { title: "Relato não encontrado", robots: { index: false } };
  const title = kindTitle(relato.kind, relato.species);
  const description = `Visto ${describeSeen(relato.seen, new Date())}. Veja a área no mapa e ajude.`;
  return {
    title,
    description,
    openGraph: { title, description, type: "article", url: `/r/${relato.id}` },
    twitter: { card: "summary_large_image", title, description },
  };
}

export default async function RelatoPage({ params }: Props) {
  const relato = await publicRelato((await params).id);
  if (!relato) notFound();
  return <RelatoDetail initial={relato} />;
}
