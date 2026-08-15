import { Link, createFileRoute } from "@tanstack/react-router";
import { Clock, ReceiptText, ShieldCheck } from "lucide-react";

import { PageHero, Section, SectionHeading, SiteLayout } from "@/components/site/Layout";
import { Button } from "@/components/ui/button";
import { DEPOSIT, GRACE_MINUTES, LATE_FEE_PER_30, PACKAGES, REPLACEMENT_FEE, RENT_STEPS } from "@/lib/jt-data";

export const Route = createFileRoute("/how-it-works")({
  head: () => ({
    meta: [
      { title: "How Juice Tech Power Bank Rentals Work" },
      {
        name: "description",
        content:
          "Scan, verify with OTP, choose a package, pay and collect. See exactly how a Juice Tech power bank rental works from start to return.",
      },
      { property: "og:title", content: "How Juice Tech Power Bank Rentals Work" },
      {
        property: "og:description",
        content: "Eight simple steps from scanning a station QR code to your return confirmation.",
      },
      { property: "og:type", content: "article" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: HowItWorks,
});

function HowItWorks() {
  return (
    <SiteLayout>
      <PageHero
        eyebrow="How it works"
        title="From flat battery to fully mobile in under a minute."
        lead="Every Juice Tech rental follows the same eight steps, whether you're at a festival, a market or a shopping centre."
      >
        <Button asChild size="lg" className="font-bold">
          <Link to="/rent-a-power-bank">Rent Now</Link>
        </Button>
      </PageHero>

      <Section>
        <ol className="grid gap-4 md:grid-cols-2">
          {RENT_STEPS.map((s, i) => (
            <li key={s} className="flex gap-4 rounded-2xl border border-border bg-card p-6">
              <span className="flex size-11 shrink-0 items-center justify-center rounded-xl bg-primary font-display text-lg font-extrabold text-primary-foreground">
                {i + 1}
              </span>
              <p className="self-center text-lg font-medium leading-snug">{s}</p>
            </li>
          ))}
        </ol>
      </Section>

      <Section tone="grey">
        <SectionHeading
          eyebrow="Pricing"
          title="What you see before you pay."
          lead="Every rental screen shows the full cost breakdown and the return deadline before payment is taken."
        />
        <div className="mt-10 grid gap-5 md:grid-cols-2">
          {PACKAGES.map((p) => (
            <div key={p.id} className="rounded-2xl border border-border bg-card p-7">
              <p className="text-sm font-bold uppercase tracking-widest text-muted-foreground">
                {p.label}
              </p>
              <p className="mt-2 font-display text-5xl font-extrabold">R{p.price}</p>
              <ul className="mt-5 grid gap-2 text-muted-foreground">
                <li className="flex items-center gap-2">
                  <Clock className="size-4 text-primary" /> {p.minutes} minutes of rental time
                </li>
                <li className="flex items-center gap-2">
                  <ShieldCheck className="size-4 text-primary" /> R{DEPOSIT} refundable deposit
                </li>
                <li className="flex items-center gap-2">
                  <ReceiptText className="size-4 text-primary" /> Receipt by email or SMS
                </li>
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-6 grid gap-4 rounded-2xl border border-border bg-card p-7 sm:grid-cols-2 lg:grid-cols-4">
          {[
            ["Refundable deposit", `R${DEPOSIT}`],
            ["Grace period", `${GRACE_MINUTES} minutes`],
            ["Late fee", `R${LATE_FEE_PER_30} / 30 min`],
            ["Replacement charge", `R${REPLACEMENT_FEE}`],
          ].map(([l, v]) => (
            <div key={l}>
              <p className="text-sm text-muted-foreground">{l}</p>
              <p className="font-display text-2xl font-extrabold">{v}</p>
            </div>
          ))}
        </div>
        <p className="mt-4 text-sm text-muted-foreground">
          Late fees never exceed the disclosed replacement value. Deposits are released once the
          station confirms the correct power bank was returned — bank processing times may affect
          when the refund reflects.
        </p>
      </Section>
    </SiteLayout>
  );
}
