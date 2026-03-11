import Link from "next/link";
import { InvoiceListItem } from "@/lib/types";
import { formatCurrency, formatDate, formatDateTime } from "@/lib/format";
import StatusBadge from "./StatusBadge";

interface Props {
  invoices: InvoiceListItem[];
  showViewAll?: boolean;
}

export default function InvoiceTable({ invoices, showViewAll }: Props) {
  if (invoices.length === 0) {
    return (
      <div className="rounded-xl p-12 text-center" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
        <svg className="w-12 h-12 mx-auto" style={{ color: "var(--text-muted)" }} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p className="mt-4" style={{ color: "var(--text-secondary)" }}>No invoices yet</p>
        <Link href="/upload" className="text-blue-500 hover:text-blue-400 text-sm mt-2 inline-block">
          Upload your first invoice
        </Link>
      </div>
    );
  }

  return (
    <div className="rounded-xl overflow-hidden" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
      <table className="w-full">
        <thead>
          <tr style={{ borderBottom: "1px solid var(--border)" }}>
            <th className="text-left text-xs font-medium uppercase tracking-wider px-6 py-3" style={{ color: "var(--text-muted)" }}>Status</th>
            <th className="text-left text-xs font-medium uppercase tracking-wider px-6 py-3" style={{ color: "var(--text-muted)" }}>Vendor</th>
            <th className="text-left text-xs font-medium uppercase tracking-wider px-6 py-3" style={{ color: "var(--text-muted)" }}>Invoice #</th>
            <th className="text-left text-xs font-medium uppercase tracking-wider px-6 py-3" style={{ color: "var(--text-muted)" }}>Job #</th>
            <th className="text-right text-xs font-medium uppercase tracking-wider px-6 py-3" style={{ color: "var(--text-muted)" }}>Amount</th>
            <th className="text-left text-xs font-medium uppercase tracking-wider px-6 py-3" style={{ color: "var(--text-muted)" }}>Date</th>
            <th className="text-left text-xs font-medium uppercase tracking-wider px-6 py-3" style={{ color: "var(--text-muted)" }}>Uploaded</th>
          </tr>
        </thead>
        <tbody>
          {invoices.map((inv) => (
            <tr key={inv.id} className="transition-colors" style={{ borderBottom: "1px solid var(--border)" }}>
              <td className="px-6 py-4">
                <StatusBadge status={inv.status} />
              </td>
              <td className="px-6 py-4">
                <Link href={`/invoices/${inv.id}`} className="text-blue-500 hover:text-blue-400 font-medium">
                  {inv.vendor_name || "Unknown Vendor"}
                </Link>
              </td>
              <td className="px-6 py-4" style={{ color: "var(--text-secondary)" }}>{inv.invoice_number || "—"}</td>
              <td className="px-6 py-4" style={{ color: "var(--text-secondary)" }}>{inv.job_number || "—"}</td>
              <td className="px-6 py-4 text-right font-medium" style={{ color: "var(--text-primary)" }}>{formatCurrency(inv.total_amount)}</td>
              <td className="px-6 py-4" style={{ color: "var(--text-secondary)" }}>{formatDate(inv.invoice_date)}</td>
              <td className="px-6 py-4 text-sm" style={{ color: "var(--text-muted)" }}>{formatDateTime(inv.created_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {showViewAll && (
        <div className="px-6 py-3" style={{ borderTop: "1px solid var(--border)" }}>
          <Link href="/invoices" className="text-sm text-blue-500 hover:text-blue-400">
            View all invoices →
          </Link>
        </div>
      )}
    </div>
  );
}
