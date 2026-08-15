/**
 * Client for the Juice Tech Python API (backend/).
 *
 * Start the API with the "Juice Tech API" run configuration in PyCharm, or:
 *   cd backend && .venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
 *
 * Set VITE_API_URL in a .env file to point at a deployed API instead.
 */

export const API_URL =
  (import.meta.env.VITE_API_URL as string | undefined) ?? "http://localhost:8000";

/** Thrown for any non-2xx response, carrying the API's own message. */
export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(
  path: string,
  options: { method?: string; body?: unknown; token?: string } = {},
): Promise<T> {
  const { method = "GET", body, token } = options;

  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });

  if (!response.ok) {
    // FastAPI puts the human-readable reason in `detail`.
    let detail = `Request failed with status ${response.status}`;
    try {
      const payload = await response.json();
      if (typeof payload?.detail === "string") detail = payload.detail;
    } catch {
      // Body was not JSON — keep the generic message.
    }
    throw new ApiError(response.status, detail);
  }

  return response.json() as Promise<T>;
}

// --- Types (mirror backend/app/schemas.py) --------------------------------

export type Station = {
  id: string;
  venue: string;
  online: boolean;
  fast_charge: boolean;
  signal: number;
  total: number;
  available: number;
  rented: number;
};

export type Package = {
  id: string;
  label: string;
  minutes: number;
  price: number;
};

export type Pricing = {
  currency: string;
  packages: Package[];
  deposit: number;
  replacement_fee: number;
  grace_minutes: number;
  late_fee_per_30: number;
};

export type Rental = {
  reference: string;
  phone: string;
  package_id: string;
  price: number;
  deposit: number;
  station_id: string;
  power_bank_id: string;
  started_at: string;
  due_at: string;
  returned_at: string | null;
  return_station_id: string | null;
  late_fee: number;
  status: "active" | "overdue" | "returned";
  minutes_remaining: number;
  minutes_overdue: number;
  total_due: number;
};

export type EnquiryPayload = {
  name: string;
  email: string;
  phone: string;
  event_type?: string;
  event_date?: string;
  message: string;
};

export type Enquiry = EnquiryPayload & {
  reference: string;
  status: string;
  created_at: string;
};

// --- Endpoints ------------------------------------------------------------

export const api = {
  health: () => request<{ status: string; service: string }>("/api/health"),

  pricing: () => request<Pricing>("/api/pricing"),

  stations: () => request<Station[]>("/api/stations"),
  station: (id: string) => request<Station>(`/api/stations/${id}`),

  requestOtp: (phone: string) =>
    request<{ phone: string; expires_in_seconds: number; message: string; debug_code?: string }>(
      "/api/otp/request",
      { method: "POST", body: { phone } },
    ),

  verifyOtp: (phone: string, code: string) =>
    request<{ token: string; phone: string; expires_at: string }>("/api/otp/verify", {
      method: "POST",
      body: { phone, code },
    }),

  startRental: (token: string, station_id: string, package_id: string) =>
    request<Rental>("/api/rentals", {
      method: "POST",
      body: { station_id, package_id },
      token,
    }),

  rental: (reference: string) => request<Rental>(`/api/rentals/${reference}`),

  returnRental: (reference: string, station_id: string) =>
    request<Rental>(`/api/rentals/${reference}/return`, {
      method: "POST",
      body: { station_id },
    }),

  myRentals: (token: string) => request<Rental[]>("/api/rentals", { token }),

  createEnquiry: (payload: EnquiryPayload) =>
    request<Enquiry>("/api/enquiries", { method: "POST", body: payload }),
};
