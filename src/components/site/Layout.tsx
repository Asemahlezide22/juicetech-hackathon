import type { ReactNode } from "react";

import { ChatWidget } from "@/components/site/ChatWidget";
import { SiteFooter } from "@/components/site/SiteFooter";
import { SiteHeader } from "@/components/site/SiteHeader";

export function SiteLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col">
      <SiteHeader />
      <main className="flex-1">{children}</main>
      <SiteFooter />
      <ChatWidget />
    </div>
  );
}

export function PageHero({
  eyebrow,
  title,
  lead,
  children,
}: {
  eyebrow?: string;
  title: string;
  lead?: string;
  children?: ReactNode;
}) {
  return (
    <section className="bg-ink text-ink-foreground">
      <div className="container-jt py-16 md:py-24">
        {eyebrow && (
          <p className="mb-4 inline-flex rounded-full bg-primary/15 px-3 py-1 text-xs font-bold uppercase tracking-widest text-primary">
            {eyebrow}
          </p>
        )}
        <h1 className="max-w-4xl text-4xl font-extrabold leading-[1.05] md:text-6xl">{title}</h1>
        {lead && <p className="mt-5 max-w-2xl text-lg text-ink-muted">{lead}</p>}
        {children && <div className="mt-8">{children}</div>}
      </div>
    </section>
  );
}

export function Section({
  tone = "light",
  children,
  className = "",
}: {
  tone?: "light" | "grey" | "ink";
  children: ReactNode;
  className?: string;
}) {
  const bg =
    tone === "ink"
      ? "bg-ink text-ink-foreground"
      : tone === "grey"
        ? "bg-muted text-foreground"
        : "bg-background text-foreground";
  return (
    <section className={`${bg} ${className}`}>
      <div className="container-jt section-pad">{children}</div>
    </section>
  );
}

export function SectionHeading({
  eyebrow,
  title,
  lead,
  invert = false,
}: {
  eyebrow?: string;
  title: string;
  lead?: string;
  invert?: boolean;
}) {
  return (
    <div className="max-w-3xl">
      {eyebrow && (
        <p className="mb-3 text-xs font-bold uppercase tracking-[0.2em] text-primary">{eyebrow}</p>
      )}
      <h2 className="text-3xl font-extrabold leading-tight md:text-4xl">{title}</h2>
      {lead && (
        <p className={`mt-4 text-lg ${invert ? "text-ink-muted" : "text-muted-foreground"}`}>{lead}</p>
      )}
    </div>
  );
}
