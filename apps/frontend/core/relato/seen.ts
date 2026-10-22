import type { TimePrecision } from "../api/client";

// Pilot city's zone; must match the backend's DEFAULT_TZ (parse_seen runs there).
export const PILOT_TZ = "America/Sao_Paulo";

type Part = "madrugada" | "manha" | "tarde" | "noite";

const PARTS: { part: Part; from: number; to: number; phrase: string }[] = [
  { part: "madrugada", from: 0, to: 6, phrase: "de madrugada" },
  { part: "manha", from: 6, to: 12, phrase: "de manhã" },
  { part: "tarde", from: 12, to: 18, phrase: "à tarde" },
  { part: "noite", from: 18, to: 24, phrase: "à noite" },
];

interface Local {
  ymd: string;
  hour: number;
  minute: number;
}

function local(date: Date, timeZone: string): Local {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
  }).formatToParts(date);
  const get = (type: string) => parts.find((p) => p.type === type)?.value ?? "00";
  return {
    ymd: `${get("year")}-${get("month")}-${get("day")}`,
    hour: Number(get("hour")),
    minute: Number(get("minute")),
  };
}

export interface SeenOption {
  /** Sent to the API as `seen_text`; null means "agora". Must be phrasing parse_seen accepts. */
  text: string | null;
  label: string;
}

/** Quick choices for "Quando você viu?", newest first, only parts of day that have started. */
export function seenOptions(now: Date, timeZone = PILOT_TZ): SeenOption[] {
  const { hour } = local(now, timeZone);
  const today = PARTS.filter((p) => p.from <= hour)
    .reverse()
    .map((p) => ({ text: `hoje ${p.phrase}`, label: `Hoje ${p.phrase}` }));
  const yesterday = [...PARTS]
    .reverse()
    .map((p) => ({ text: `ontem ${p.phrase}`, label: `Ontem ${p.phrase}` }));
  return [
    { text: null, label: "Agora" },
    { text: "agora há pouco", label: "Há pouco (última hora)" },
    ...today,
    ...yesterday,
  ];
}

function dayWord(date: Date, now: Date, timeZone: string): string {
  const day = local(date, timeZone).ymd;
  if (day === local(now, timeZone).ymd) return "hoje";
  if (day === local(new Date(now.getTime() - 86_400_000), timeZone).ymd) return "ontem";
  const [, m, d] = day.split("-");
  return `${d}/${m}`;
}

/** "ontem à tarde", "hoje, entre 15h e 16h", "há 20 min" — never finer than the API gave. */
export function describeSeen(
  seen: { start: string; end: string; precision: TimePrecision },
  now: Date,
  timeZone = PILOT_TZ,
): string {
  const start = new Date(seen.start);
  const end = new Date(seen.end);
  const day = dayWord(start, now, timeZone);
  const from = local(start, timeZone).hour;
  const lastMinute = new Date(end.getTime() - 60_000);
  const to = local(lastMinute, timeZone).hour + 1;
  const sameDay = local(start, timeZone).ymd === local(lastMinute, timeZone).ymd;

  switch (seen.precision) {
    case "part_of_day": {
      const part = PARTS.find((p) => p.from === from && p.to === to);
      if (part && sameDay) return `${day} ${part.phrase}`;
      return sameDay ? `${day}, entre ${from}h e ${to}h` : `${day}, a partir das ${from}h`;
    }
    case "hour":
      return `${day}, entre ${from}h e ${to}h`;
    case "day":
      return day;
    default: {
      const minutesAgo = Math.round((now.getTime() - end.getTime()) / 60_000);
      if (minutesAgo < 1) return "agora";
      if (minutesAgo < 60) return `há ${minutesAgo} min`;
      if (minutesAgo < 180) return `há ${Math.round(minutesAgo / 60)} h`;
      const { hour, minute } = local(end, timeZone);
      return `${day}, ${hour}h${String(minute).padStart(2, "0")}`;
    }
  }
}
