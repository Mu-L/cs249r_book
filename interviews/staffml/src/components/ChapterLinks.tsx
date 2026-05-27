"use client";

import { BookOpen, ExternalLink } from "lucide-react";
import { getChaptersForArea, type ChapterRef } from "@/lib/chapters";

interface ChapterLinksProps {
  area: string;
}

export default function ChapterLinks({ area }: ChapterLinksProps) {
  const chapters = getChaptersForArea(area);
  if (chapters.length === 0) return null;

  return (
    <div className="flex flex-wrap items-center gap-2 mt-3 text-xs">
      <span className="flex items-center gap-1 text-textTertiary">
        <BookOpen className="w-3 h-3" />
        Read more:
      </span>
      {chapters.map((ch: ChapterRef) => (
        <a
          key={`${ch.vol}-${ch.slug}`}
          href={ch.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md
                     bg-accentBlue/5 text-accentBlue hover:bg-accentBlue/10
                     border border-accentBlue/10 transition-colors"
        >
          Vol.{ch.vol}: {ch.title}
          <ExternalLink className="w-2.5 h-2.5 opacity-50" />
        </a>
      ))}
    </div>
  );
}
