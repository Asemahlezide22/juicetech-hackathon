import { MessageCircle, Send, X } from "lucide-react";
import { useState } from "react";

import { JuiceTechMark } from "@/components/brand/JuiceTechLogo";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { BRAND } from "@/lib/jt-data";

type Msg = { from: "bot" | "user"; text: string };

const KB: { match: RegExp; answer: string }[] = [
  { match: /price|cost|how much|rate/i, answer: "Rentals are R150 for 1 hour and R250 for 2 hours. A refundable R500 deposit is held and released once the power bank is returned." },
  { match: /rent|start|scan|qr/i, answer: "Scan the QR code on any Juice Tech station, verify your cellphone number with an OTP, choose a package, pay securely and collect the power bank the station releases." },
  { match: /pay|payfast|card|eft|capitec|apple|google/i, answer: "We use Payfast: debit and credit cards, Capitec Pay, Instant EFT, Apple Pay, Google Pay and QR payment. Staffed events also accept tap to pay and chip and PIN." },
  { match: /return|give back/i, answer: "Slide the power bank into any empty slot at a Juice Tech station until it clicks. Your rental ends once the station confirms the return and you get a receipt." },
  { match: /deposit|refund/i, answer: "The R500 deposit is refundable and released on confirmed return. Bank processing times may affect when it reflects." },
  { match: /late|overdue/i, answer: "A 15-minute grace period applies, then R75 per additional 30 minutes. Late fees never exceed the disclosed replacement value." },
  { match: /event|hire|festival/i, answer: "Event hire starts at R3,500 for one station for up to 8 hours with 12 power banks, delivery, setup and remote monitoring in Cape Town." },
  { match: /advert|screen|sponsor/i, answer: "Our station screens run image and video adverts by venue, station and display hour. Campaigns are approved before going live." },
  { match: /franchis/i, answer: "Juice Tech supplies stations, power banks, technology, training and sales support to approved franchise partners. Submit the franchise form to start." },
  { match: /contact|phone|email|support|human|person|agent/i, answer: `You can reach our team on ${BRAND.email}, ${BRAND.phone}, or chat to a person on WhatsApp ${BRAND.whatsapp}.` },
  { match: /station|location|where/i, answer: "Station availability is shown live on the station screen and in the rental page after you scan its QR code — I can't confirm stock for a specific station myself." },
];

const ESCALATE = /dispute|charged twice|fraud|stolen|burn|hot|swollen|fire|injur|unsafe|complain/i;

function answerFor(text: string): string {
  if (ESCALATE.test(text)) {
    return `This needs a human on it right away. Please chat to our team on WhatsApp ${BRAND.whatsapp} — we'll open a support ticket and review your payment, rental and station records.`;
  }
  const hit = KB.find((k) => k.match.test(text));
  return (
    hit?.answer ??
    `I can help with rentals, pricing, returns, deposits, event hire, advertising and franchising. For anything else, chat to a person on WhatsApp ${BRAND.whatsapp}.`
  );
}

export function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [msgs, setMsgs] = useState<Msg[]>([
    { from: "bot", text: "Hi! I'm the Juice Tech assistant. Ask me about rentals, pricing, returns, event hire, advertising or franchising." },
  ]);

  function send(e: React.FormEvent) {
    e.preventDefault();
    const text = input.trim();
    if (!text) return;
    setMsgs((m) => [...m, { from: "user", text }, { from: "bot", text: answerFor(text) }]);
    setInput("");
  }

  return (
    <>
      {open && (
        <div className="fixed bottom-24 right-4 z-50 flex h-[26rem] w-[min(22rem,calc(100vw-2rem))] flex-col overflow-hidden rounded-2xl border border-border bg-card shadow-2xl">
          <div className="flex items-center gap-2.5 bg-ink px-4 py-3 text-ink-foreground">
            <JuiceTechMark className="size-6" />
            <div className="flex-1">
              <p className="font-display text-sm font-bold">Juice Tech Assistant</p>
              <p className="text-xs text-ink-muted">Typically replies instantly</p>
            </div>
            <button aria-label="Close chat" onClick={() => setOpen(false)}>
              <X className="size-4" />
            </button>
          </div>

          <div className="flex-1 space-y-3 overflow-y-auto p-4">
            {msgs.map((m, i) => (
              <div
                key={i}
                className={
                  m.from === "user"
                    ? "ml-auto max-w-[85%] rounded-2xl rounded-br-sm bg-primary px-3.5 py-2.5 text-sm text-primary-foreground"
                    : "mr-auto max-w-[90%] rounded-2xl rounded-bl-sm bg-muted px-3.5 py-2.5 text-sm text-foreground"
                }
              >
                {m.text}
              </div>
            ))}
          </div>

          <a
            href={BRAND.whatsappHref}
            target="_blank"
            rel="noreferrer"
            className="border-t border-border bg-muted px-4 py-2.5 text-center text-xs font-semibold text-foreground hover:text-primary"
          >
            Talk to a person — WhatsApp {BRAND.whatsapp}
          </a>

          <form onSubmit={send} className="flex items-center gap-2 border-t border-border p-3">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question…"
              aria-label="Message"
            />
            <Button type="submit" size="icon" aria-label="Send">
              <Send className="size-4" />
            </Button>
          </form>
        </div>
      )}

      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-label="Open Juice Tech chat"
        className="fixed bottom-5 right-4 z-50 flex size-14 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-xl transition-transform hover:scale-105"
      >
        <MessageCircle className="size-6" />
      </button>
    </>
  );
}
