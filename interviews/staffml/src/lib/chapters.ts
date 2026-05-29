import chapterMap from "@/data/chapter-map.json";

export interface ChapterRef {
  vol: number;
  slug: string;
  title: string;
  section: string | null;
  url: string;
}

const BASE = chapterMap.baseUrl;
const areaMap = chapterMap.areaToChapters as Record<
  string,
  { vol: number; slug: string; title: string; section: string | null }[]
>;

export function getChaptersForArea(area: string): ChapterRef[] {
  const entries = areaMap[area];
  if (!entries) return [];
  return entries.map((e) => ({
    ...e,
    url: `${BASE}/vol${e.vol}/${e.slug}/${e.section ? "#" + e.section : ""}`,
  }));
}
