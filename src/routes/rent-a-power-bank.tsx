import { Link, createFileRoute } from "@tanstack/react-router";
import { QrCode } from "lucide-react";

import { PageHero, Section, SectionHeading, SiteLayout } from "@/components/site/Layout";
import { LiveStationCard } from "@/components/site/StationCard";
import { Button } from "@/components/ui/button";
import { DEMO_STATION, DEPOSIT, GRACE_MINUTES, LATE_FEE_PER_30, PACKAGES, REPLACEMENT_FEE } from "@/lib/jt-data";

export const Route = createFileRoute("/rent-a-power-bank")({
  head: () => ({
    meta: [
      { title: "Rent a Power Bank | Juice Tech" },
      {
        name: "description",
        content:
          "Rent a fast-charging power bank for R150 an hour or R250 for two hours. Scan a Juice Tech station QR code and stay connected.",
      },
      { property: "og:title", content: "Rent a Power Bank | Juice Tech" },
      { property: "og:description", content: "R150 for one hour, R250 for two hours, R500 refundable deposit." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: RentPage,
});

function RentPage() {
  return (
    <SiteLayout>
      <PageHero
        eyebrow="Rent now"
        title="Scan a station. Keep moving."
        lead="Find a Juice Tech station, scan its QR code with your phone camera and your rental starts on the spot. No app download needed."
      >
        <div className="grid gap-6 lg:grid-cols-[1fr_20rem] lg:items-start">
          <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-7">
            <QrCode className="size-10 text-primary" />
            <h2 className="mt-4 text-2xl font-bold">No station nearby?</h2>
            <p className="mt-2 text-ink-muted">
              Try the live demo rental journey using our test station {DEMO_STATION.id} at{" "}
              {DEMO_STATION.venue}. All payments are simulated and clearly labelled as Demo.
            </p>
            <Button asChild size="lg" className="mt-6 font-bold">
              <Link to="/rent/$stationId" params={{ stationId: DEMO_STATION.id }}>
                Start demo rental
              </Link>
            </Button>
          </div>
          <LiveStationCard />
        </div>
      </PageHero>

      <Section>
        <SectionHeading eyebrow="Pricing" title="Simple, upfront pricing." />
        <div className="mt-8 grid gap-5 md:grid-cols-2">
          {PACKAGES.map((p) => (
            <div key={p.id} className="rounded-2xl border-2 border-foreground bg-card p-7">
              <p className="text-sm font-bold uppercase tracking-widest text-muted-foreground">{p.label}</p>
              <p className="mt-1 font-display text-5xl font-extrabold">R{p.price}</p>
              <p className="mt-3 text-muted-foreground">
                Plus a R{DEPOSIT} refundable security deposit, released once the power bank is returned.
              </p>
            </div>
          ))}
        </div>
        <p className="mt-6 text-sm text-muted-foreground">
          {GRACE_MINUTES}-minute grace period. Late returns are charged R{LATE_FEE_PER_30} per additional 30
          minutes, capped at the R{REPLACEMENT_FEE} replacement value. Read the full{" "}
          <Link to="/terms" className="font-semibold underline">
            rental terms
          </Link>
          .
        </p>
      </Section>
    </SiteLayout>
  );
}
