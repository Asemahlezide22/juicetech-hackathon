import { Link } from "@tanstack/react-router";
import { Menu, X } from "lucide-react";
import { useState } from "react";

import { JuiceTechLogo } from "@/components/brand/JuiceTechLogo";
import { Button } from "@/components/ui/button";
import { NAV } from "@/lib/jt-data";

export function SiteHeader() {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-ink/95 text-ink-foreground backdrop-blur">
      <div className="container-jt flex h-16 items-center justify-between gap-4">
        <Link to="/" className="shrink-0" aria-label="Juice Tech home">
          <JuiceTechLogo tone="default" className="[&_.text-foreground]:text-ink-foreground" />
        </Link>

        <nav className="hidden items-center gap-1 xl:flex">
          {NAV.slice(1).map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className="rounded-md px-2.5 py-2 text-sm font-medium text-ink-muted transition-colors hover:text-primary"
              activeProps={{ className: "text-primary" }}
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <Link to="/staff-login" className="hidden text-sm font-medium text-ink-muted hover:text-primary md:block">
            Staff Login
          </Link>
          <Button asChild size="sm" className="font-semibold">
            <Link to="/rent-a-power-bank">Rent Now</Link>
          </Button>
          <button
            type="button"
            className="rounded-md p-2 text-ink-foreground xl:hidden"
            aria-label={open ? "Close menu" : "Open menu"}
            onClick={() => setOpen((v) => !v)}
          >
            {open ? <X className="size-5" /> : <Menu className="size-5" />}
          </button>
        </div>
      </div>

      {open && (
        <nav className="border-t border-white/10 bg-ink xl:hidden">
          <div className="container-jt grid gap-1 py-4">
            {NAV.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                onClick={() => setOpen(false)}
                className="rounded-lg px-3 py-2.5 text-base font-medium text-ink-muted hover:bg-white/5 hover:text-primary"
                activeProps={{ className: "text-primary" }}
              >
                {item.label}
              </Link>
            ))}
            <Link
              to="/staff-login"
              onClick={() => setOpen(false)}
              className="rounded-lg px-3 py-2.5 text-base font-medium text-ink-muted hover:bg-white/5 hover:text-primary"
            >
              Staff Login
            </Link>
          </div>
        </nav>
      )}
    </header>
  );
}
