import { BatteryCharging, QrCode, Signal, Zap } from "lucide-react";

import { DEMO_STATION } from "@/lib/jt-data";

export function LiveStationCard({ className = "" }: { className?: string }) {
  const s = DEMO_STATION;
  return (
    <div
      className={`rounded-3xl border border-white/10 bg-white/[0.06] p-6 backdrop-blur ${className}`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="relative flex size-2.5">
            <span className="absolute inline-flex size-full animate-ping rounded-full bg-success opacity-75" />
            <span className="relative inline-flex size-2.5 rounded-full bg-success" />
          </span>
          <span className="text-sm font-bold uppercase tracking-widest text-success">Station online</span>
        </div>
        <span className="font-display text-xs font-bold text-ink-muted">{s.id}</span>
      </div>

      <p className="mt-4 text-sm text-ink-muted">{s.venue}</p>

      <div className="mt-5 grid grid-cols-2 gap-3">
        <Stat label="Available" value={s.available} icon={<BatteryCharging className="size-4" />} accent />
        <Stat label="Rented" value={s.rented} icon={<Zap className="size-4" />} />
      </div>

      <div className="mt-5 flex items-center gap-2 rounded-xl bg-primary/15 px-3.5 py-2.5 text-sm font-semibold text-primary">
        <Zap className="size-4 animate-charge-pulse" />
        Fast charging available
      </div>

      <div className="mt-4 flex items-center justify-between border-t border-white/10 pt-4 text-sm text-ink-muted">
        <span className="flex items-center gap-2">
          <QrCode className="size-4 text-primary" /> Scan QR code to begin
        </span>
        <span className="flex items-center gap-1.5">
          <Signal className="size-4 text-primary" /> {s.signal}/5
        </span>
      </div>
    </div>
  );
}

function Stat({
  label,
  value,
  icon,
  accent,
}: {
  label: string;
  value: number;
  icon: React.ReactNode;
  accent?: boolean;
}) {
  return (
    <div className="rounded-2xl bg-black/40 p-4">
      <div className={`flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider ${accent ? "text-primary" : "text-ink-muted"}`}>
        {icon}
        {label}
      </div>
      <p className="mt-1 font-display text-3xl font-extrabold text-ink-foreground">{value}</p>
    </div>
  );
}
