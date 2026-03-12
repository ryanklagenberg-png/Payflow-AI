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
  coding_status: "predicted" | "confirmed" | "manual" | null;
  coding_confidence: number | null;
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

export interface CodingAlternative {
  job_number: string | null;
  cost_code: string | null;
  confidence: number;
  reasoning: string;
}

export interface CodingPrediction {
  predicted_job_number: string | null;
  predicted_cost_code: string | null;
  confidence: number;
  method: string;
  reasoning: string;
  alternatives: CodingAlternative[];
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
  coding_predictions: CodingPrediction | null;
  coding_status: "predicted" | "confirmed" | "manual" | null;
  coding_confidence: number | null;
  coding_method: string | null;
  line_items: LineItem[];
  updated_at: string;
}

export interface UploadResponse {
  id: string;
  status: string;
  file_name: string;
  message: string;
}
