import { useState } from "react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

export type Field = {
  name: string;
  label: string;
  type?: "text" | "email" | "tel" | "date" | "time" | "number" | "textarea" | "select" | "checkbox" | "file";
  options?: string[];
  required?: boolean;
  full?: boolean;
};

function reference(prefix: string) {
  return `${prefix}-${Date.now().toString(36).toUpperCase().slice(-6)}`;
}

export function EnquiryForm({
  fields,
  refPrefix,
  submitLabel = "Send Enquiry",
  consentLabel,
}: {
  fields: Field[];
  refPrefix: string;
  submitLabel?: string;
  consentLabel?: string;
}) {
  const [sent, setSent] = useState<string | null>(null);
  const [consent, setConsent] = useState(false);

  function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (consentLabel && !consent) {
      toast.error("Please tick the consent box before submitting.");
      return;
    }
    const r = reference(refPrefix);
    setSent(r);
    toast.success(`Enquiry received — reference ${r}`, {
      description: "Demo mode: a confirmation would be emailed to you and to info@juicetech.co.za.",
    });
    e.currentTarget.reset();
  }

  if (sent) {
    return (
      <div className="rounded-2xl border border-border bg-card p-8 text-center">
        <p className="text-xs font-bold uppercase tracking-widest text-primary">Demo submission</p>
        <h3 className="mt-2 text-2xl font-extrabold">Thank you — we're on it.</h3>
        <p className="mt-3 text-muted-foreground">
          Your reference number is{" "}
          <span className="font-display font-bold text-foreground">{sent}</span>. A confirmation goes to
          you and an alert to info@juicetech.co.za, and the enquiry is logged as{" "}
          <strong>New</strong> on the staff dashboard.
        </p>
        <Button variant="outline" className="mt-6" onClick={() => setSent(null)}>
          Submit another enquiry
        </Button>
      </div>
    );
  }

  return (
    <form onSubmit={onSubmit} className="rounded-2xl border border-border bg-card p-6 md:p-8">
      <div className="grid gap-5 sm:grid-cols-2">
        {fields.map((f) => (
          <div key={f.name} className={f.full || f.type === "textarea" ? "sm:col-span-2" : ""}>
            <Label htmlFor={f.name} className="mb-2 block text-sm font-semibold">
              {f.label}
              {f.required && <span className="text-destructive"> *</span>}
            </Label>
            {f.type === "textarea" ? (
              <Textarea id={f.name} name={f.name} required={f.required} rows={4} />
            ) : f.type === "select" ? (
              <select
                id={f.name}
                name={f.name}
                required={f.required}
                className="h-10 w-full rounded-md border border-input bg-background px-3 text-sm"
                defaultValue=""
              >
                <option value="" disabled>
                  Select…
                </option>
                {f.options?.map((o) => (
                  <option key={o} value={o}>
                    {o}
                  </option>
                ))}
              </select>
            ) : (
              <Input id={f.name} name={f.name} type={f.type ?? "text"} required={f.required} />
            )}
          </div>
        ))}
      </div>

      {consentLabel && (
        <label className="mt-6 flex items-start gap-3 text-sm text-muted-foreground">
          <Checkbox checked={consent} onCheckedChange={(v) => setConsent(v === true)} className="mt-0.5" />
          <span>{consentLabel}</span>
        </label>
      )}

      <Button type="submit" size="lg" className="mt-6 w-full font-semibold sm:w-auto">
        {submitLabel}
      </Button>
    </form>
  );
}
