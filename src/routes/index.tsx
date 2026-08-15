import { Link, createFileRoute } from "@tanstack/react-router";
import {
  BatteryWarning,
  Building2,
  CreditCard,
  Mail,
  MapPin,
  MessageCircle,
  MonitorPlay,
  Phone,
  ShieldCheck,
  Sparkles,
  Zap,
} from "lucide-react";

import stationHero from "@/assets/station-hero.jpg";
import { EnquiryForm } from "@/components/site/EnquiryForm";
import { PageHero, Section, SectionHeading, SiteLayout } from "@/components/site/Layout";
import { LiveStationCard } from "@/components/site/StationCard";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";
import { BRAND, FAQS, PACKAGES, RENT_STEPS } from "@/lib/jt-data";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Juice Tech | Power Bank Rentals & Event Charging, Cape Town" },
      {
        name: "description",
        content:
          "Rent a fast-charging power bank from a Juice Tech station. Stay Powered. Stay Limitless. Event charging hire and digital screen advertising across South Africa.",
      },
      { property: "og:title", content: "Juice Tech | Pay for the time, share the time." },
      {
        property: "og:description",
        content:
          "Smart power bank rentals, event charging hire and digital screen advertising in Cape Town.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Home,
});

function Home() {
  return (
    <SiteLayout>
      {/* HERO */}
      <section className="relative overflow-hidden bg-ink text-ink-foreground">
        <div className="pointer-events-none absolute -left-40 top-10 size-[32rem] rounded-full bg-primary/10 blur-3xl" />
        <div className="container-jt relative grid gap-12 py-14 md:py-20 lg:grid-cols-[1.05fr_0.95fr] lg:items-center">
          <div>
            <p className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-3.5 py-1.5 text-xs font-bold uppercase tracking-[0.18em] text-primary">
              <Zap className="size-3.5" /> {BRAND.tagline}
            </p>
            <h1 className="mt-6 text-[2.6rem] font-extrabold leading-[1.02] sm:text-6xl lg:text-[4.2rem]">
              Never let a low battery{" "}
              <span className="text-primary">end your experience.</span>
            </h1>
            <p className="mt-6 max-w-xl text-lg text-ink-muted sm:text-xl">
              Rent a fast-charging Juice Tech power bank, stay connected and keep moving. Pay for the
              time, share the time.
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <Button asChild size="lg" className="h-13 px-7 text-base font-bold">
                <Link to="/rent-a-power-bank">Rent Now</Link>
              </Button>
              <Button
                asChild
                size="lg"
                variant="outline"
                className="h-13 border-white/25 bg-transparent px-7 text-base font-bold text-ink-foreground hover:bg-white/10 hover:text-primary"
              >
                <Link to="/event-hire">Book Juice Tech for an Event</Link>
              </Button>
            </div>

            <dl className="mt-10 grid max-w-lg grid-cols-3 gap-4 border-t border-white/10 pt-6">
              {[
                ["R150", "1 hour rental"],
                ["3-in-1", "Built-in cables"],
                ["24/7", "Station monitoring"],
              ].map(([v, l]) => (
                <div key={l}>
                  <dt className="font-display text-2xl font-extrabold text-primary">{v}</dt>
                  <dd className="text-sm text-ink-muted">{l}</dd>
                </div>
              ))}
            </dl>
          </div>

          <div className="relative">
            <img
              src={stationHero}
              alt="Juice Tech black and yellow charging station with power banks at an outdoor event"
              width={1280}
              height={1600}
              className="mx-auto w-full max-w-md rounded-3xl object-cover shadow-2xl"
            />
            <LiveStationCard className="mx-auto mt-6 max-w-md lg:absolute lg:-left-10 lg:bottom-8 lg:mt-0 lg:w-72" />
          </div>
        </div>
      </section>

      {/* PROBLEM */}
      <Section>
        <SectionHeading
          eyebrow="The problem"
          title="A dead phone is more than an inconvenience."
          lead="At events, markets and public spaces, a flat battery cuts people off exactly when they need to be connected."
        />
        <div className="mt-10 grid gap-5 md:grid-cols-3">
          {[
            {
              icon: BatteryWarning,
              title: "Cut off when it matters",
              body: "No transport, no digital tickets, no mobile payments and no way to reach the people you came with.",
            },
            {
              icon: ShieldCheck,
              title: "A safety risk",
              body: "A phone with no charge means no way to call for help, share a location or contact emergency services.",
            },
            {
              icon: Sparkles,
              title: "Moments lost",
              body: "The photos, videos and memories of the day stop the second the battery does.",
            },
          ].map((c) => (
            <article
              key={c.title}
              className="rounded-2xl border border-border bg-card p-6 transition-shadow hover:shadow-lg"
            >
              <span className="inline-flex size-11 items-center justify-center rounded-xl bg-primary text-primary-foreground">
                <c.icon className="size-5" />
              </span>
              <h3 className="mt-4 text-xl font-bold">{c.title}</h3>
              <p className="mt-2 text-muted-foreground">{c.body}</p>
            </article>
          ))}
        </div>
      </Section>

      {/* HOW IT WORKS */}
      <Section tone="grey">
        <SectionHeading
          eyebrow="How renting works"
          title="Scan, verify, pay, charge — under a minute."
        />
        <ol className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {RENT_STEPS.map((s, i) => (
            <li key={s} className="rounded-2xl border border-border bg-card p-5">
              <span className="font-display text-3xl font-extrabold text-primary">
                {String(i + 1).padStart(2, "0")}
              </span>
              <p className="mt-2 font-medium leading-snug">{s}</p>
            </li>
          ))}
        </ol>
        <div className="mt-8 flex flex-wrap gap-3">
          {PACKAGES.map((p) => (
            <div
              key={p.id}
              className="flex items-center gap-3 rounded-xl border border-border bg-card px-5 py-3"
            >
              <Zap className="size-5 text-primary" />
              <span className="font-display text-lg font-bold">R{p.price}</span>
              <span className="text-muted-foreground">/ {p.label.toLowerCase()}</span>
            </div>
          ))}
          <Button asChild size="lg" className="font-semibold">
            <Link to="/rent-a-power-bank">Start a rental</Link>
          </Button>
        </div>
      </Section>

      {/* SAFETY */}
      <Section tone="ink">
        <div className="grid gap-10 lg:grid-cols-2 lg:items-center">
          <SectionHeading
            invert
            eyebrow="Safety and connectivity"
            title="Staying charged is staying safe."
            lead="Every rental is tied to a verified cellphone number, a unique battery ID and a unique order number, with audit logs on every action."
          />
          <ul className="grid gap-3 sm:grid-cols-2">
            {[
              "OTP cellphone verification",
              "Payment confirmed before release",
              "Refundable R500 deposit",
              "Unique customer-to-battery assignment",
              "Automated return reminders",
              "Staff alerts and audit logs",
            ].map((t) => (
              <li
                key={t}
                className="flex items-start gap-3 rounded-xl border border-white/10 bg-white/[0.04] p-4 text-sm font-medium"
              >
                <ShieldCheck className="mt-0.5 size-4 shrink-0 text-primary" />
                {t}
              </li>
            ))}
          </ul>
        </div>
      </Section>

      {/* THREE PILLARS */}
      <Section>
        <div className="grid gap-5 md:grid-cols-3">
          {[
            {
              icon: Building2,
              title: "Event hire",
              body: "Stations, power banks, delivery, setup, collection and remote monitoring for your event. From R3,500.",
              to: "/event-hire" as const,
              cta: "See event packages",
            },
            {
              icon: MonitorPlay,
              title: "Digital advertising",
              body: "Large station screens running brand adverts, sponsor messages, schedules and safety notices.",
              to: "/advertising" as const,
              cta: "Advertise with us",
            },
            {
              icon: CreditCard,
              title: "Franchising",
              body: "Equipment, technology, training and sales support to run Juice Tech in your city.",
              to: "/franchising" as const,
              cta: "Explore franchising",
            },
          ].map((c) => (
            <article key={c.title} className="group rounded-2xl bg-ink p-7 text-ink-foreground">
              <span className="inline-flex size-11 items-center justify-center rounded-xl bg-primary text-primary-foreground">
                <c.icon className="size-5" />
              </span>
              <h3 className="mt-4 text-xl font-bold">{c.title}</h3>
              <p className="mt-2 text-ink-muted">{c.body}</p>
              <Link
                to={c.to}
                className="mt-5 inline-flex items-center gap-2 font-semibold text-primary group-hover:gap-3"
              >
                {c.cta} <span aria-hidden>→</span>
              </Link>
            </article>
          ))}
        </div>
      </Section>

      {/* FAQ */}
      <Section tone="grey">
        <SectionHeading eyebrow="FAQ" title="Frequently asked questions" />
        <Accordion type="single" collapsible className="mt-8 max-w-3xl">
          {FAQS.map((f) => (
            <AccordionItem key={f.q} value={f.q}>
              <AccordionTrigger className="text-left text-base font-semibold">{f.q}</AccordionTrigger>
              <AccordionContent className="text-base text-muted-foreground">{f.a}</AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </Section>

      {/* CONTACT */}
      <Section>
        <div className="grid gap-10 lg:grid-cols-[0.9fr_1.1fr]">
          <div>
            <SectionHeading
              eyebrow="Contact"
              title="Talk to the Juice Tech team."
              lead="Event hire, advertising, franchising or support — we reply fast."
            />
            <ul className="mt-8 grid gap-4 text-base">
              <li className="flex items-center gap-3">
                <Mail className="size-5 text-primary" />
                <a href={`mailto:${BRAND.email}`} className="font-medium hover:text-primary">
                  {BRAND.email}
                </a>
              </li>
              <li className="flex items-center gap-3">
                <Phone className="size-5 text-primary" />
                <a href={BRAND.phoneHref} className="font-medium hover:text-primary">
                  {BRAND.phone}
                </a>
              </li>
              <li className="flex items-center gap-3">
                <MessageCircle className="size-5 text-primary" />
                <a href={BRAND.whatsappHref} className="font-medium hover:text-primary">
                  WhatsApp {BRAND.whatsapp}
                </a>
              </li>
              <li className="flex items-center gap-3">
                <MapPin className="size-5 text-primary" />
                <span className="font-medium">{BRAND.location}</span>
              </li>
            </ul>
          </div>
          <EnquiryForm
            refPrefix="JT"
            fields={[
              { name: "name", label: "Name", required: true },
              { name: "company", label: "Company name" },
              { name: "email", label: "Email", type: "email", required: true },
              { name: "phone", label: "Contact number", type: "tel", required: true },
              {
                name: "type",
                label: "Enquiry type",
                type: "select",
                required: true,
                options: ["General", "Event hire", "Advertising", "Franchising", "Support"],
              },
              { name: "message", label: "Enquiry message", type: "textarea", required: true },
            ]}
            consentLabel="I consent to Juice Tech processing my information to respond to this enquiry."
          />
        </div>
      </Section>
    </SiteLayout>
  );
}
