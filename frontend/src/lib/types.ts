export interface InvoiceListItem {
  id: string;
  status: "uploaded" | "processing" | "extracted" | "approved" | "rejected" | "failed";
  file_name: string;
  vendor_name: string | null;
  invoice_number: string | null;
  total_amount: number | null;
  invoice_date: string | null;
  job_number: string | null;
  cost_code: string | null;
  po_number: string | null;
  created_at: string;
}

export interface LineItem {
  id: string;
  line_number: number;
  description: string;
  quantity: number | null;
  unit_price: number | null;
  amount: number | null;
}

export interface InvoiceDetail extends InvoiceListItem {
  vendor_address: string | null;
  due_date: string | null;
  job_number: string | null;
  cost_code: string | null;
  po_number: string | null;
  subtotal: number | null;
  tax_amount: number | null;
  currency: string;
  payment_terms: string | null;
  confidence_score: number | null;
  line_items: LineItem[];
  updated_at: string;
}

export interface UploadResponse {
  id: string;
  status: string;
  file_name: string;
  message: string;
}
