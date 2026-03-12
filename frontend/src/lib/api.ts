import { InvoiceDetail, InvoiceListItem, UploadResponse } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function authHeaders(): Record<string, string> {
  const token = typeof window !== "undefined" ? localStorage.getItem("payflow_token") : null;
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function fetchInvoices(params?: {
  status?: string;
  skip?: number;
  limit?: number;
  search?: string;
  job_number?: string;
}): Promise<{ items: InvoiceListItem[]; total: number }> {
  const searchParams = new URLSearchParams();
  if (params?.status) searchParams.set("status", params.status);
  if (params?.skip) searchParams.set("skip", String(params.skip));
  if (params?.limit) searchParams.set("limit", String(params.limit));
  if (params?.search) searchParams.set("search", params.search);
  if (params?.job_number) searchParams.set("job_number", params.job_number);

  const query = searchParams.toString();
  const res = await fetch(`${API_URL}/api/v1/invoices${query ? `?${query}` : ""}`, {
    cache: "no-store",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch invoices");
  return res.json();
}

export async function fetchInvoice(id: string): Promise<InvoiceDetail> {
  const res = await fetch(`${API_URL}/api/v1/invoices/${id}`, {
    cache: "no-store",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch invoice");
  return res.json();
}

export async function updateInvoice(id: string, updates: Record<string, unknown>): Promise<InvoiceDetail> {
  const res = await fetch(`${API_URL}/api/v1/invoices/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(updates),
  });
  if (!res.ok) throw new Error("Update failed");
  return res.json();
}

export async function uploadInvoice(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_URL}/api/v1/invoices/upload`, {
    method: "POST",
    headers: authHeaders(),
    body: formData,
  });
  if (!res.ok) throw new Error("Upload failed");
  return res.json();
}

export async function uploadInvoicesBulk(files: File[]): Promise<UploadResponse[]> {
  const formData = new FormData();
  for (const file of files) {
    formData.append("files", file);
  }

  const res = await fetch(`${API_URL}/api/v1/invoices/upload-bulk`, {
    method: "POST",
    headers: authHeaders(),
    body: formData,
  });
  if (!res.ok) throw new Error("Bulk upload failed");
  return res.json();
}

export async function deleteInvoice(id: string): Promise<void> {
  const res = await fetch(`${API_URL}/api/v1/invoices/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Delete failed");
}

export async function updateInvoiceStatus(id: string, status: string): Promise<{ id: string; status: string }> {
  const res = await fetch(`${API_URL}/api/v1/invoices/${id}/status`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ status }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Status update failed" }));
    throw new Error(err.detail || "Status update failed");
  }
  return res.json();
}

export function getExportCsvUrl(status?: string): string {
  const params = status ? `?status=${status}` : "";
  return `${API_URL}/api/v1/invoices/export/csv${params}`;
}

export interface DuplicateGroup {
  match_type: "invoice_number" | "vendor_amount_date";
  invoices: {
    id: string;
    vendor_name: string | null;
    invoice_number: string | null;
    total_amount: number | null;
    invoice_date: string | null;
    status: string;
    file_name: string;
    created_at: string;
  }[];
}

export async function fetchDuplicates(): Promise<DuplicateGroup[]> {
  const res = await fetch(`${API_URL}/api/v1/invoices/duplicates`, {
    cache: "no-store",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch duplicates");
  return res.json();
}

export interface DashboardStats {
  status_breakdown: { name: string; value: number }[];
  vendor_spend: { name: string; amount: number }[];
  weekly_volume: { week: string; count: number }[];
  division_spend: { name: string; amount: number }[];
  top_jobs: { job_number: string; amount: number }[];
}

export async function fetchStats(): Promise<DashboardStats> {
  const res = await fetch(`${API_URL}/api/v1/invoices/stats`, {
    cache: "no-store",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch stats");
  return res.json();
}

export async function confirmCoding(id: string): Promise<InvoiceDetail> {
  const res = await fetch(`${API_URL}/api/v1/invoices/${id}/confirm-coding`, {
    method: "POST",
    headers: authHeaders(),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Confirm coding failed" }));
    throw new Error(err.detail || "Confirm coding failed");
  }
  return res.json();
}

export async function selectCodingAlternative(
  id: string,
  jobNumber: string | null,
  costCode: string | null
): Promise<InvoiceDetail> {
  const res = await fetch(`${API_URL}/api/v1/invoices/${id}/select-coding`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ job_number: jobNumber, cost_code: costCode }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Select coding failed" }));
    throw new Error(err.detail || "Select coding failed");
  }
  return res.json();
}

export async function reExtractInvoice(id: string): Promise<{ id: string; status: string; confidence_score: number; message: string }> {
  const res = await fetch(`${API_URL}/api/v1/invoices/${id}/re-extract`, {
    method: "POST",
    headers: authHeaders(),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Re-extraction failed" }));
    throw new Error(err.detail || "Re-extraction failed");
  }
  return res.json();
}

export interface AuditEntry {
  id: string;
  action: string;
  details: string | null;
  previous_value: Record<string, unknown> | null;
  new_value: Record<string, unknown> | null;
  user_email: string | null;
  created_at: string;
}

export async function fetchAuditLog(invoiceId: string): Promise<AuditEntry[]> {
  const res = await fetch(`${API_URL}/api/v1/invoices/${invoiceId}/audit`, {
    cache: "no-store",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Failed to fetch audit log");
  return res.json();
}
