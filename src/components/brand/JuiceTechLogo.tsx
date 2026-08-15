import { cn } from "@/lib/utils";

type Tone = "default" | "mono-light" | "mono-dark";

function toneColors(tone: Tone) {
  if (tone === "mono-light") return { bolt: "var(--jt-bolt-light)", cell: "var(--jt-cell-light)" };
  if (tone === "mono-dark") return { bolt: "var(--jt-bolt-dark)", cell: "var(--jt-cell-dark)" };
  return { bolt: "var(--jt-bolt)", cell: "var(--jt-cell)" };
}

/**
 * Standalone "JT" mark: a battery cell whose interior is cut by a lightning
 * bolt, with the cell's left rail reading as a J stem and the terminal cap
 * reading as a T crossbar.
 */
export function JuiceTechMark({
  className,
  tone = "default",
}: {
  className?: string;
  tone?: Tone;
}) {
  const c = toneColors(tone);
  return (
    <svg
      viewBox="0 0 64 64"
      role="img"
      aria-label="Juice Tech"
      className={cn("block", className)}
      fill="none"
    >
      {/* terminal cap / T crossbar */}
      <rect x="18" y="2" width="28" height="8" rx="2.5" fill={c.cell} />
      {/* cell body */}
      <rect x="8" y="12" width="48" height="50" rx="12" fill={c.cell} />
      {/* bolt cut-out */}
      <path
        d="M36.5 18 L20 40.5 h9.5 L27.5 56 L45 33 h-10 z"
        fill={c.bolt}
        stroke={c.cell}
        strokeWidth="2.5"
        strokeLinejoin="round"
      />
      {/* J hook: notch out of the lower-left rail */}
      <path d="M8 44 h12 v6 a6 6 0 0 1 -6 6 H8 z" fill={c.bolt} />
    </svg>
  );
}

export function JuiceTechLogo({
  className,
  tone = "default",
  showWordmark = true,
}: {
  className?: string;
  tone?: Tone;
  showWordmark?: boolean;
}) {
  return (
    <span className={cn("inline-flex items-center gap-2.5", className)}>
      <JuiceTechMark tone={tone} className="h-8 w-8 shrink-0" />
      {showWordmark && (
        <span className="font-display text-xl font-extrabold leading-none tracking-tight">
          <span className="text-primary">JUICE</span>{" "}
          <span className="text-foreground">TECH</span>
        </span>
      )}
    </span>
  );
}
