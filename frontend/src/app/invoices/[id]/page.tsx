"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { fetchInvoice, deleteInvoice, updateInvoice, updateInvoiceStatus, fetchDuplicates, reExtractInvoice, fetchAuditLog, confirmCoding, selectCodingAlternative, DuplicateGroup, AuditEntry } from "@/lib/api";
import { formatCurrency, formatDate, formatDateTime } from "@/lib/format";
import { InvoiceDetail } from "@/lib/types";
import StatusBadge from "@/components/StatusBadge";
import ConfidenceMeter from "@/components/ConfidenceMeter";
import PdfViewer from "@/components/PdfViewer";
import { useToast } from "@/components/ToastProvider";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function InvoiceDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { toast } = useToast();
  const [invoice, setInvoice] = useState<InvoiceDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"details" | "lines" | "audit">("details");
  const [deleting, setDeleting] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [editFields, setEditFields] = useState<Record<string, string>>({});
  const [duplicateInvoices, setDuplicateInvoices] = useState<DuplicateGroup["invoices"]>([]);
  const [reExtracting, setReExtracting] = useState(false);
  const [auditLog, setAuditLog] = useState<AuditEntry[]>([]);
  const [confirmingCoding, setConfirmingCoding] = useState(false);
  const [showAlternatives, setShowAlternatives] = useState(false);

  const handleDelete = async () => {
    if (!invoice) return;
    setDeleting(true);
    try {
      await deleteInvoice(invoice.id);
      toast("Invoice deleted");
      router.push("/invoices");
    } catch {
      setDeleting(false);
      setShowDeleteConfirm(false);
    }
  };

  const handleStatusChange = async (newStatus: string) => {
    if (!invoice) return;
    try {
      await updateInvoiceStatus(invoice.id, newStatus);
      setInvoice({ ...invoice, status: newStatus as InvoiceDetail["status"] });
      toast(`Invoice ${newStatus}`);
      fetchAuditLog(invoice.id).then(setAuditLog).catch(() => {});
    } catch {
      toast("Failed to update status", "error");
    }
  };

  const handleReExtract = async () => {
    if (!invoice) return;
    setReExtracting(true);
    setError(null);
    try {
      await reExtractInvoice(invoice.id);
      const updated = await fetchInvoice(invoice.id);
      setInvoice(updated);
      toast("Re-extraction complete");
      fetchAuditLog(invoice.id).then(setAuditLog).catch(() => {});
    } catch (e) {
      toast(e instanceof Error ? e.message : "Re-extraction failed", "error");
    } finally {
      setReExtracting(false);
    }
  };

  const handleConfirmCoding = async () => {
    if (!invoice) return;
    setConfirmingCoding(true);
    try {
      const updated = await confirmCoding(invoice.id);
      setInvoice(updated);
      toast("Coding confirmed");
      fetchAuditLog(invoice.id).then(setAuditLog).catch(() => {});
    } catch {
      toast("Failed to confirm coding", "error");
    } finally {
      setConfirmingCoding(false);
    }
  };

  const handleSelectAlternative = async (jobNumber: string | null, costCode: string | null) => {
    if (!invoice) return;
    setConfirmingCoding(true);
    try {
      const updated = await selectCodingAlternative(invoice.id, jobNumber, costCode);
      setInvoice(updated);
      setShowAlternatives(false);
      toast("Alternative coding applied");
      fetchAuditLog(invoice.id).then(setAuditLog).catch(() => {});
    } catch {
      toast("Failed to apply coding", "error");
    } finally {
      setConfirmingCoding(false);
    }
  };

  const canApprove = invoice?.status === "extracted" || invoice?.status === "rejected";
  const canReject = invoice?.status === "extracted" || invoice?.status === "approved";
  const canReExtract = invoice?.status === "failed" || invoice?.status === "extracted";

  const startEditing = () => {
    if (!invoice) return;
    setEditFields({
      vendor_name: invoice.vendor_name || "",
      vendor_address: invoice.vendor_address || "",
      invoice_number: invoice.invoice_number || "",
      invoice_date: invoice.invoice_date || "",
      due_date: invoice.due_date || "",
      job_number: invoice.job_number || "",
      cost_code: invoice.cost_code || "",
      po_number: invoice.po_number || "",
      payment_terms: invoice.payment_terms || "",
      currency: invoice.currency || "USD",
      subtotal: invoice.subtotal != null ? String(invoice.subtotal) : "",
      tax_amount: invoice.tax_amount != null ? String(invoice.tax_amount) : "",
      total_amount: invoice.total_amount != null ? String(invoice.total_amount) : "",
    });
    setEditing(true);
  };

  const cancelEditing = () => {
    setEditing(false);
    setEditFields({});
  };

  const handleSave = async () => {
    if (!invoice) return;
    setSaving(true);
    try {
      const updates: Record<string, unknown> = {};
      const stringFields = ["vendor_name", "vendor_address", "invoice_number", "job_number", "cost_code", "po_number", "payment_terms", "currency"];
      const dateFields = ["invoice_date", "due_date"];
      const numberFields = ["subtotal", "tax_amount", "total_amount"];

      for (const key of stringFields) {
        updates[key] = editFields[key] || null;
      }
      for (const key of dateFields) {
        updates[key] = editFields[key] || null;
      }
      for (const key of numberFields) {
        updates[key] = editFields[key] ? parseFloat(editFields[key]) : null;
      }

      const updated = await updateInvoice(invoice.id, updates);
      setInvoice(updated);
      setEditing(false);
      toast("Changes saved");
      fetchAuditLog(invoice.id).then(setAuditLog).catch(() => {});
    } catch {
      toast("Failed to save changes", "error");
    } finally {
      setSaving(false);
    }
  };

  const updateField = (key: string, value: string) => {
    setEditFields((prev) => ({ ...prev, [key]: value }));
  };

  useEffect(() => {
    if (!params.id) return;
    const id = params.id as string;
    fetchInvoice(id)
      .then((inv) => {
        setInvoice(inv);
        // Fetch audit log
        fetchAuditLog(inv.id).then(setAuditLog).catch(() => {});
        // Check for duplicates involving this invoice
        fetchDuplicates().then((groups) => {
          for (const group of groups) {
            const match = group.invoices.find((i) => i.id === inv.id);
            if (match) {
              setDuplicateInvoices(group.invoices.filter((i) => i.id !== inv.id));
              break;
            }
          }
        }).catch(() => {});
      })
      .catch(() => setError("Invoice not found"))
      .finally(() => setLoading(false));
  }, [params.id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (error || !invoice) {
    return (
      <div className="text-center py-16">
        <p className="text-red-400">{error || "Invoice not found"}</p>
        <Link href="/invoices" className="text-blue-500 hover:text-blue-400 text-sm mt-4 inline-block">
          ← Back to invoices
        </Link>
      </div>
    );
  }

  const fileUrl = `${API_URL}/api/v1/invoices/${invoice.id}/file`;
  const isPdf = invoice.file_name.toLowerCase().endsWith(".pdf");

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <Link href="/invoices" className="text-sm inline-flex items-center gap-1 text-blue-500 hover:text-blue-400">
          ← Back to invoices
        </Link>
        <div className="flex items-center gap-3">
          <StatusBadge status={invoice.status} />
          <div className="w-32">
            <ConfidenceMeter score={invoice.confidence_score} />
          </div>
          {!editing && canApprove && (
            <button
              onClick={() => handleStatusChange("approved")}
              className="px-3 py-1.5 rounded-lg text-sm font-medium bg-emerald-600 hover:bg-emerald-500 text-white transition-colors"
            >
              Approve
            </button>
          )}
          {!editing && canReject && (
            <button
              onClick={() => handleStatusChange("rejected")}
              className="px-3 py-1.5 rounded-lg text-sm font-medium bg-orange-600 hover:bg-orange-500 text-white transition-colors"
            >
              Reject
            </button>
          )}
          {!editing ? (
            <button
              onClick={startEditing}
              className="px-3 py-1.5 rounded-lg text-sm font-medium text-blue-400 hover:bg-blue-500/10 transition-colors"
            >
              Edit
            </button>
          ) : (
            <>
              <button
                onClick={cancelEditing}
                disabled={saving}
                className="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
                style={{ color: "var(--text-secondary)" }}
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                disabled={saving}
                className="px-3 py-1.5 rounded-lg text-sm font-medium bg-blue-600 hover:bg-blue-500 text-white transition-colors disabled:opacity-50"
              >
                {saving ? "Saving..." : "Save"}
              </button>
            </>
          )}
          {!editing && canReExtract && (
            <button
              onClick={handleReExtract}
              disabled={reExtracting}
              className="px-3 py-1.5 rounded-lg text-sm font-medium text-amber-400 hover:bg-amber-500/10 transition-colors disabled:opacity-50"
            >
              {reExtracting ? "Re-extracting..." : "Re-extract"}
            </button>
          )}
          <button
            onClick={() => setShowDeleteConfirm(true)}
            className="px-3 py-1.5 rounded-lg text-sm font-medium text-red-400 hover:bg-red-500/10 transition-colors"
          >
            Delete
          </button>
        </div>
      </div>

      {/* Duplicate Warning */}
      {duplicateInvoices.length > 0 && (
        <div className="rounded-lg px-4 py-3 flex items-start gap-3 bg-amber-500/10 border border-amber-500/20">
          <svg className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div>
            <p className="text-sm font-medium text-amber-400">Potential Duplicate Detected</p>
            <div className="mt-1 space-y-1">
              {duplicateInvoices.map((dup) => (
                <p key={dup.id} className="text-xs" style={{ color: "var(--text-secondary)" }}>
                  Matches{" "}
                  <Link href={`/invoices/${dup.id}`} className="text-blue-500 hover:text-blue-400">
                    {dup.vendor_name || dup.file_name}
                  </Link>
                  {dup.invoice_number ? ` (${dup.invoice_number})` : ""}
                  {dup.total_amount ? ` — ${formatCurrency(dup.total_amount)}` : ""}
                </p>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Side-by-side layout */}
      <div className="flex gap-4" style={{ height: "calc(100vh - 140px)" }}>

        {/* Left: PDF/Image Viewer */}
        <div className="w-1/2 rounded-xl overflow-hidden flex flex-col" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
          <div className="px-4 py-3 flex items-center justify-between" style={{ borderBottom: "1px solid var(--border)" }}>
            <span className="text-sm font-medium" style={{ color: "var(--text-primary)" }}>
              {invoice.file_name}
            </span>
            <a
              href={fileUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-blue-500 hover:text-blue-400"
            >
              Open in new tab
            </a>
          </div>
          <div className="flex-1">
            {isPdf ? (
              <PdfViewer url={fileUrl} />
            ) : (
              <div className="w-full h-full flex items-center justify-center p-4" style={{ background: "#1a1a1a" }}>
                <img
                  src={fileUrl}
                  alt="Invoice"
                  className="max-w-full max-h-full object-contain"
                />
              </div>
            )}
          </div>
        </div>

        {/* Right: Extracted Data */}
        <div className="w-1/2 overflow-y-auto space-y-4">

          {/* Vendor Header */}
          <div className="rounded-xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            {editing ? (
              <div className="space-y-3">
                <EditInput label="Vendor Name" value={editFields.vendor_name} onChange={(v) => updateField("vendor_name", v)} />
                <EditInput label="Vendor Address" value={editFields.vendor_address} onChange={(v) => updateField("vendor_address", v)} />
              </div>
            ) : (
              <>
                <h1 className="text-xl font-bold" style={{ color: "var(--text-primary)" }}>
                  {invoice.vendor_name || "Unknown Vendor"}
                </h1>
                {invoice.vendor_address && (
                  <p className="text-sm mt-1" style={{ color: "var(--text-secondary)" }}>{invoice.vendor_address}</p>
                )}
              </>
            )}
          </div>

          {/* Tabs */}
          <div className="flex gap-1 rounded-lg p-1" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <button
              onClick={() => setActiveTab("details")}
              className={`flex-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                activeTab === "details" ? "bg-blue-600 text-white" : ""
              }`}
              style={activeTab !== "details" ? { color: "var(--text-secondary)" } : undefined}
            >
              Details
            </button>
            <button
              onClick={() => setActiveTab("lines")}
              className={`flex-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                activeTab === "lines" ? "bg-blue-600 text-white" : ""
              }`}
              style={activeTab !== "lines" ? { color: "var(--text-secondary)" } : undefined}
            >
              Line Items ({invoice.line_items.length})
            </button>
            <button
              onClick={() => setActiveTab("audit")}
              className={`flex-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                activeTab === "audit" ? "bg-blue-600 text-white" : ""
              }`}
              style={activeTab !== "audit" ? { color: "var(--text-secondary)" } : undefined}
            >
              History ({auditLog.length})
            </button>
          </div>

          {activeTab === "details" && (
            <>
              {/* Job / Cost Coding */}
              <div className="rounded-xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-medium" style={{ color: "var(--text-muted)" }}>JOB COST CODING</h3>
                  {invoice.coding_status && (
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                      invoice.coding_status === "confirmed" ? "bg-emerald-500/15 text-emerald-400" :
                      invoice.coding_status === "predicted" ? "bg-blue-500/15 text-blue-400" :
                      "bg-slate-500/15 text-slate-400"
                    }`}>
                      {invoice.coding_status === "predicted" ? "AI Predicted" :
                       invoice.coding_status === "confirmed" ? "AI Confirmed" :
                       "Manually Coded"}
                    </span>
                  )}
                </div>
                {editing ? (
                  <div className="grid grid-cols-3 gap-4">
                    <EditInput label="Job Number" value={editFields.job_number} onChange={(v) => updateField("job_number", v)} />
                    <EditInput label="Cost Code" value={editFields.cost_code} onChange={(v) => updateField("cost_code", v)} />
                    <EditInput label="PO Number" value={editFields.po_number} onChange={(v) => updateField("po_number", v)} />
                  </div>
                ) : (
                  <>
                    <div className="grid grid-cols-3 gap-5">
                      <Field label="Job Number" value={invoice.job_number} />
                      <Field label="Cost Code" value={invoice.cost_code} />
                      <Field label="PO Number" value={invoice.po_number} />
                    </div>

                    {/* AI Coding Prediction Panel */}
                    {invoice.coding_status === "predicted" && invoice.coding_predictions && (
                      <div className="mt-4 pt-4" style={{ borderTop: "1px solid var(--border)" }}>
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-2">
                            <svg className="w-4 h-4 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                              <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
                            </svg>
                            <span className="text-xs font-medium text-blue-400">
                              {Math.round(invoice.coding_predictions.confidence * 100)}% confident
                              {invoice.coding_method && ` — ${invoice.coding_method.replace(/_/g, " ")}`}
                            </span>
                          </div>
                          <div className="flex items-center gap-2">
                            {invoice.coding_predictions.alternatives?.length > 0 && (
                              <button
                                onClick={() => setShowAlternatives(!showAlternatives)}
                                className="text-xs text-slate-400 hover:text-slate-300 transition-colors"
                              >
                                {showAlternatives ? "Hide" : "Show"} alternatives ({invoice.coding_predictions.alternatives.length})
                              </button>
                            )}
                            <button
                              onClick={handleConfirmCoding}
                              disabled={confirmingCoding}
                              className="px-3 py-1 rounded-md text-xs font-medium bg-blue-600 hover:bg-blue-500 text-white transition-colors disabled:opacity-50"
                            >
                              {confirmingCoding ? "..." : "Confirm"}
                            </button>
                          </div>
                        </div>
                        <p className="text-xs" style={{ color: "var(--text-secondary)" }}>
                          {invoice.coding_predictions.reasoning}
                        </p>

                        {/* Alternatives */}
                        {showAlternatives && invoice.coding_predictions.alternatives?.length > 0 && (
                          <div className="mt-3 space-y-2">
                            {invoice.coding_predictions.alternatives.map((alt, idx) => (
                              <div
                                key={idx}
                                className="flex items-center justify-between rounded-lg px-3 py-2"
                                style={{ background: "var(--bg-input)", border: "1px solid var(--border)" }}
                              >
                                <div>
                                  <span className="text-xs font-medium" style={{ color: "var(--text-primary)" }}>
                                    {alt.job_number || "—"} / {alt.cost_code || "—"}
                                  </span>
                                  <span className="text-xs ml-2" style={{ color: "var(--text-muted)" }}>
                                    ({Math.round(alt.confidence * 100)}%)
                                  </span>
                                  <p className="text-xs mt-0.5" style={{ color: "var(--text-secondary)" }}>
                                    {alt.reasoning}
                                  </p>
                                </div>
                                <button
                                  onClick={() => handleSelectAlternative(alt.job_number, alt.cost_code)}
                                  disabled={confirmingCoding}
                                  className="text-xs px-2 py-1 rounded text-blue-400 hover:bg-blue-500/10 transition-colors flex-shrink-0 ml-2"
                                >
                                  Use this
                                </button>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}
                  </>
                )}
              </div>

              {/* Invoice Fields */}
              <div className="rounded-xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
                {editing ? (
                  <div className="grid grid-cols-2 gap-4">
                    <EditInput label="Invoice #" value={editFields.invoice_number} onChange={(v) => updateField("invoice_number", v)} />
                    <EditInput label="Invoice Date" value={editFields.invoice_date} onChange={(v) => updateField("invoice_date", v)} type="date" />
                    <EditInput label="Due Date" value={editFields.due_date} onChange={(v) => updateField("due_date", v)} type="date" />
                    <EditInput label="Payment Terms" value={editFields.payment_terms} onChange={(v) => updateField("payment_terms", v)} />
                    <EditInput label="Currency" value={editFields.currency} onChange={(v) => updateField("currency", v)} />
                  </div>
                ) : (
                  <div className="grid grid-cols-2 gap-5">
                    <Field label="Invoice #" value={invoice.invoice_number} />
                    <Field label="Invoice Date" value={formatDate(invoice.invoice_date)} />
                    <Field label="Due Date" value={formatDate(invoice.due_date)} />
                    <Field label="Payment Terms" value={invoice.payment_terms} />
                    <Field label="Currency" value={invoice.currency} />
                  </div>
                )}
              </div>

              {/* Financial Summary */}
              <div className="rounded-xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
                <h3 className="text-sm font-medium mb-4" style={{ color: "var(--text-muted)" }}>FINANCIAL SUMMARY</h3>
                {editing ? (
                  <div className="space-y-3">
                    <EditInput label="Subtotal" value={editFields.subtotal} onChange={(v) => updateField("subtotal", v)} type="number" />
                    <EditInput label="Tax" value={editFields.tax_amount} onChange={(v) => updateField("tax_amount", v)} type="number" />
                    <EditInput label="Total" value={editFields.total_amount} onChange={(v) => updateField("total_amount", v)} type="number" />
                  </div>
                ) : (
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span style={{ color: "var(--text-secondary)" }}>Subtotal</span>
                      <span className="font-medium" style={{ color: "var(--text-primary)" }}>{formatCurrency(invoice.subtotal)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span style={{ color: "var(--text-secondary)" }}>Tax</span>
                      <span className="font-medium" style={{ color: "var(--text-primary)" }}>{formatCurrency(invoice.tax_amount)}</span>
                    </div>
                    <div className="pt-3 flex justify-between" style={{ borderTop: "1px solid var(--border)" }}>
                      <span className="font-semibold text-blue-500">Total</span>
                      <span className="font-bold text-lg text-blue-500">{formatCurrency(invoice.total_amount)}</span>
                    </div>
                  </div>
                )}
              </div>
            </>
          )}

          {activeTab === "lines" && invoice.line_items.length > 0 && (
            <div className="rounded-xl overflow-hidden" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
              <table className="w-full">
                <thead>
                  <tr style={{ borderBottom: "1px solid var(--border)" }}>
                    <th className="text-left text-xs font-medium uppercase tracking-wider px-4 py-3" style={{ color: "var(--text-muted)" }}>#</th>
                    <th className="text-left text-xs font-medium uppercase tracking-wider px-4 py-3" style={{ color: "var(--text-muted)" }}>Description</th>
                    <th className="text-right text-xs font-medium uppercase tracking-wider px-4 py-3" style={{ color: "var(--text-muted)" }}>Qty</th>
                    <th className="text-right text-xs font-medium uppercase tracking-wider px-4 py-3" style={{ color: "var(--text-muted)" }}>Price</th>
                    <th className="text-right text-xs font-medium uppercase tracking-wider px-4 py-3" style={{ color: "var(--text-muted)" }}>Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {invoice.line_items.map((item) => (
                    <tr key={item.id} style={{ borderBottom: "1px solid var(--border)" }}>
                      <td className="px-4 py-3 text-sm" style={{ color: "var(--text-muted)" }}>{item.line_number}</td>
                      <td className="px-4 py-3 text-sm" style={{ color: "var(--text-primary)" }}>{item.description}</td>
                      <td className="px-4 py-3 text-sm text-right" style={{ color: "var(--text-secondary)" }}>{item.quantity ?? "—"}</td>
                      <td className="px-4 py-3 text-sm text-right" style={{ color: "var(--text-secondary)" }}>{formatCurrency(item.unit_price)}</td>
                      <td className="px-4 py-3 text-sm text-right font-medium" style={{ color: "var(--text-primary)" }}>{formatCurrency(item.amount)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {activeTab === "audit" && (
            <div className="rounded-xl overflow-hidden" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
              {auditLog.length === 0 ? (
                <div className="p-8 text-center text-sm" style={{ color: "var(--text-muted)" }}>
                  No activity recorded yet
                </div>
              ) : (
                <div className="divide-y" style={{ borderColor: "var(--border)" }}>
                  {auditLog.map((entry) => (
                    <div key={entry.id} className="px-4 py-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <AuditIcon action={entry.action} />
                          <span className="text-sm font-medium capitalize" style={{ color: "var(--text-primary)" }}>
                            {entry.action.replace(/[_-]/g, " ")}
                          </span>
                        </div>
                        <span className="text-xs" style={{ color: "var(--text-muted)" }}>
                          {formatDateTime(entry.created_at)}
                        </span>
                      </div>
                      {entry.details && (
                        <p className="text-xs mt-1 ml-6" style={{ color: "var(--text-secondary)" }}>
                          {entry.details}
                        </p>
                      )}
                      {entry.user_email && (
                        <p className="text-xs mt-0.5 ml-6" style={{ color: "var(--text-muted)" }}>
                          by {entry.user_email}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* File Info */}
          <div className="text-xs" style={{ color: "var(--text-muted)" }}>
            Uploaded: {formatDate(invoice.created_at)}
          </div>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="rounded-xl p-6 w-96 space-y-4" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <h3 className="text-lg font-semibold" style={{ color: "var(--text-primary)" }}>Delete Invoice</h3>
            <p className="text-sm" style={{ color: "var(--text-secondary)" }}>
              Are you sure you want to delete <strong>{invoice.invoice_number || invoice.file_name}</strong>? This action cannot be undone.
            </p>
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setShowDeleteConfirm(false)}
                disabled={deleting}
                className="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                style={{ color: "var(--text-secondary)", border: "1px solid var(--border)" }}
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                disabled={deleting}
                className="px-4 py-2 rounded-lg text-sm font-medium bg-red-600 hover:bg-red-700 text-white transition-colors disabled:opacity-50"
              >
                {deleting ? "Deleting..." : "Delete"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Field({ label, value }: { label: string; value: string | null | undefined }) {
  return (
    <div>
      <p className="text-xs uppercase tracking-wider" style={{ color: "var(--text-muted)" }}>{label}</p>
      <p className="font-medium mt-1" style={{ color: "var(--text-primary)" }}>{value || "—"}</p>
    </div>
  );
}

function EditInput({
  label,
  value,
  onChange,
  type = "text",
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  type?: "text" | "date" | "number";
}) {
  return (
    <div>
      <label className="text-xs uppercase tracking-wider block mb-1" style={{ color: "var(--text-muted)" }}>
        {label}
      </label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        step={type === "number" ? "0.01" : undefined}
        className="w-full rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
        style={{ background: "var(--bg-input)", border: "1px solid var(--border)", color: "var(--text-primary)" }}
      />
    </div>
  );
}

const AUDIT_ICONS: Record<string, { color: string; path: string }> = {
  extracted: { color: "text-blue-400", path: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" },
  approved: { color: "text-emerald-400", path: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" },
  rejected: { color: "text-red-400", path: "M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" },
  edited: { color: "text-amber-400", path: "M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" },
  deleted: { color: "text-red-400", path: "M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" },
  "re-extracted": { color: "text-purple-400", path: "M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" },
  extraction_failed: { color: "text-red-400", path: "M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" },
  "re-extraction_failed": { color: "text-red-400", path: "M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" },
  coded: { color: "text-indigo-400", path: "M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" },
  coding_confirmed: { color: "text-emerald-400", path: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" },
};

function AuditIcon({ action }: { action: string }) {
  const icon = AUDIT_ICONS[action] || { color: "text-slate-400", path: "M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" };
  return (
    <svg className={`w-4 h-4 ${icon.color} flex-shrink-0`} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d={icon.path} />
    </svg>
  );
}
