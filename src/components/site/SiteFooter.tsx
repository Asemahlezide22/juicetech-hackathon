import { Link } from "@tanstack/react-router";
import { Mail, MapPin, MessageCircle, Phone } from "lucide-react";

import { JuiceTechLogo } from "@/components/brand/JuiceTechLogo";
import { BRAND, NAV } from "@/lib/jt-data";

export function SiteFooter() {
  return (
    <footer className="bg-ink text-ink-foreground">
      <div className="container-jt grid gap-10 py-14 md:grid-cols-[1.4fr_1fr_1fr]">
        <div>
          <JuiceTechLogo className="[&_.text-foreground]:text-ink-foreground" />
          <p className="mt-4 max-w-sm text-sm text-ink-muted">
            {BRAND.taglineAlt} Smart power bank rentals, event charging and digital
            screen advertising across South Africa.
          </p>
          <p className="mt-4 font-display text-sm font-bold text-primary">{BRAND.tagline}</p>
        </div>

        <div>
          <h3 className="text-sm font-bold uppercase tracking-widest text-ink-muted">Explore</h3>
          <ul className="mt-4 grid gap-2 text-sm">
            {NAV.map((item) => (
              <li key={item.to}>
                <Link to={item.to} className="text-ink-foreground/80 hover:text-primary">
                  {item.label}
                </Link>
              </li>
            ))}
            <li>
              <Link to="/terms" className="text-ink-foreground/80 hover:text-primary">
                Terms & Conditions
              </Link>
            </li>
          </ul>
        </div>

        <div>
          <h3 className="text-sm font-bold uppercase tracking-widest text-ink-muted">Contact</h3>
          <ul className="mt-4 grid gap-3 text-sm">
            <li className="flex items-center gap-2.5">
              <Mail className="size-4 text-primary" />
              <a href={`mailto:${BRAND.email}`} className="hover:text-primary">
                {BRAND.email}
              </a>
            </li>
            <li className="flex items-center gap-2.5">
              <Phone className="size-4 text-primary" />
              <a href={BRAND.phoneHref} className="hover:text-primary">
                {BRAND.phone}
              </a>
            </li>
            <li className="flex items-center gap-2.5">
              <MessageCircle className="size-4 text-primary" />
              <a href={BRAND.whatsappHref} className="hover:text-primary">
                WhatsApp {BRAND.whatsapp}
              </a>
            </li>
            <li className="flex items-center gap-2.5">
              <MapPin className="size-4 text-primary" />
              {BRAND.location}
            </li>
          </ul>
        </div>
      </div>

      <div className="border-t border-white/10">
        <div className="container-jt flex flex-col gap-2 py-5 text-xs text-ink-muted sm:flex-row sm:items-center sm:justify-between">
          <span>© {new Date().getFullYear()} Juice Tech. All rights reserved.</span>
          <span>Demo environment — all transactions are simulated.</span>
        </div>
      </div>
    </footer>
  );
}
