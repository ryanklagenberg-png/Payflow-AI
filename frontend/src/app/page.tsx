"use client";

import { useEffect, useState } from "react";
import { fetchInvoices, fetchStats, fetchDuplicates, updateInvoiceStatus, DashboardStats, DuplicateGroup } from "@/lib/api";
import { formatCurrency } from "@/lib/format";
import { InvoiceListItem } from "@/lib/types";
import Link from "next/link";
import StatCard from "@/components/StatCard";
import InvoiceTable from "@/components/InvoiceTable";
import StatusChart from "@/components/charts/StatusChart";
import VendorSpendChart from "@/components/charts/VendorSpendChart";
import VolumeChart from "@/components/charts/VolumeChart";
import DivisionSpendChart from "@/components/charts/DivisionSpendChart";
import { useToast } from "@/components/ToastProvider";

export default function DashboardPage() {
  const [invoices, setInvoices] = useState<InvoiceListItem[]>([]);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [duplicates, setDuplicates] = useState<DuplicateGroup[]>([]);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();

  useEffect(() => {
    Promise.all([
      fetchInvoices({ limit: 50 }),
      fetchStats(),
      fetchDuplicates(),
    ])
      .then(([invResult, st, dup]) => {
        setInvoices(invResult.items);
        setStats(st);
        setDuplicates(dup);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const totalValue = invoices.reduce((sum, inv) => sum + (inv.total_amount || 0), 0);
  const approved = invoices.filter((inv) => inv.status === "approved").length;
  const pendingReview = invoices.filter((inv) => inv.status === "extracted").length;
  const rejected = invoices.filter((inv) => inv.status === "rejected").length;
  const failed = invoices.filter((inv) => inv.status === "failed").length;
  const recent = invoices.slice(0, 10);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold" style={{ color: "var(--text-primary)" }}>Dashboard</h1>
        <p className="text-sm mt-1" style={{ color: "var(--text-secondary)" }}>Overview of your invoice processing pipeline</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <StatCard
          label="Total Invoices"
          value={String(invoices.length)}
          icon="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          color="bg-blue-500/10 text-blue-400"
        />
        <StatCard
          label="Total Value"
          value={formatCurrency(totalValue)}
          icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          color="bg-green-500/10 text-green-400"
        />
        <StatCard
          label="Pending Review"
          value={String(pendingReview)}
          icon="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
          color="bg-amber-500/10 text-amber-400"
          href="/invoices?status=extracted"
        />
        <StatCard
          label="Approved"
          value={String(approved)}
          icon="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
          color="bg-emerald-500/10 text-emerald-400"
          href="/invoices?status=approved"
        />
        <StatCard
          label="Rejected"
          value={String(rejected + failed)}
          icon="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
          color="bg-red-500/10 text-red-400"
          href="/invoices?status=rejected"
        />
      </div>

      {/* Charts */}
      {stats && (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <div className="rounded-xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
              <h3 className="text-sm font-medium mb-4" style={{ color: "var(--text-muted)" }}>STATUS BREAKDOWN</h3>
              <StatusChart data={stats.status_breakdown} />
            </div>
            <div className="rounded-xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
              <h3 className="text-sm font-medium mb-4" style={{ color: "var(--text-muted)" }}>TOP VENDORS BY SPEND</h3>
              <VendorSpendChart data={stats.vendor_spend} />
            </div>
            <div className="rounded-xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
              <h3 className="text-sm font-medium mb-4" style={{ color: "var(--text-muted)" }}>WEEKLY VOLUME</h3>
              <VolumeChart data={stats.weekly_volume} />
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {/* Spend by Division */}
            {stats.division_spend && stats.division_spend.length > 0 && (
              <div className="rounded-xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
                <h3 className="text-sm font-medium mb-4" style={{ color: "var(--text-muted)" }}>SPEND BY DIVISION</h3>
                <DivisionSpendChart data={stats.division_spend} />
              </div>
            )}

            {/* Top Jobs by Spend */}
            {stats.top_jobs && stats.top_jobs.length > 0 && (
              <div className="rounded-xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
                <h3 className="text-sm font-medium mb-4" style={{ color: "var(--text-muted)" }}>TOP JOBS BY SPEND</h3>
                <div className="space-y-3">
                  {stats.top_jobs.map((job, i) => (
                    <div key={job.job_number} className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <span className="text-xs font-mono w-6 text-right" style={{ color: "var(--text-muted)" }}>
                          {i + 1}.
                        </span>
                        <Link
                          href={`/invoices?status=all&job_number=${encodeURIComponent(job.job_number)}`}
                          className="text-sm font-medium text-blue-500 hover:text-blue-400"
                        >
                          {job.job_number}
                        </Link>
                      </div>
                      <span className="text-sm font-medium" style={{ color: "var(--text-primary)" }}>
                        {formatCurrency(job.amount)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </>
      )}

      {/* Pending Review Queue */}
      {pendingReview > 0 && (
        <div>
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2" style={{ color: "var(--text-primary)" }}>
            <svg className="w-5 h-5 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Pending Review ({pendingReview})
          </h2>
          <div className="rounded-xl overflow-hidden" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <table className="w-full">
              <thead>
                <tr style={{ borderBottom: "1px solid var(--border)" }}>
                  <th className="text-left text-xs font-medium uppercase tracking-wider px-6 py-3" style={{ color: "var(--text-muted)" }}>Vendor</th>
                  <th className="text-left text-xs font-medium uppercase tracking-wider px-6 py-3" style={{ color: "var(--text-muted)" }}>Invoice #</th>
                  <th className="text-right text-xs font-medium uppercase tracking-wider px-6 py-3" style={{ color: "var(--text-muted)" }}>Amount</th>
                  <th className="text-right text-xs font-medium uppercase tracking-wider px-6 py-3" style={{ color: "var(--text-muted)" }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {invoices
                  .filter((inv) => inv.status === "extracted")
                  .map((inv) => (
                    <tr key={inv.id} style={{ borderBottom: "1px solid var(--border)" }}>
                      <td className="px-6 py-4">
                        <Link href={`/invoices/${inv.id}`} className="text-blue-500 hover:text-blue-400 font-medium">
                          {inv.vendor_name || "Unknown Vendor"}
                        </Link>
                      </td>
                      <td className="px-6 py-4" style={{ color: "var(--text-secondary)" }}>{inv.invoice_number || "---"}</td>
                      <td className="px-6 py-4 text-right font-medium" style={{ color: "var(--text-primary)" }}>{formatCurrency(inv.total_amount)}</td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <button
                            onClick={async () => {
                              try {
                                await updateInvoiceStatus(inv.id, "approved");
                                setInvoices((prev) => prev.map((i) => i.id === inv.id ? { ...i, status: "approved" as const } : i));
                                toast("Invoice approved");
                              } catch { toast("Failed to approve", "error"); }
                            }}
                            className="px-3 py-1 rounded-md text-xs font-medium bg-emerald-600 hover:bg-emerald-500 text-white transition-colors"
                          >
                            Approve
                          </button>
                          <button
                            onClick={async () => {
                              try {
                                await updateInvoiceStatus(inv.id, "rejected");
                                setInvoices((prev) => prev.map((i) => i.id === inv.id ? { ...i, status: "rejected" as const } : i));
                                toast("Invoice rejected");
                              } catch { toast("Failed to reject", "error"); }
                            }}
                            className="px-3 py-1 rounded-md text-xs font-medium bg-orange-600 hover:bg-orange-500 text-white transition-colors"
                          >
                            Reject
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Duplicate Alerts */}
      {duplicates.length > 0 && (
        <div>
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2" style={{ color: "var(--text-primary)" }}>
            <svg className="w-5 h-5 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            Potential Duplicates ({duplicates.length})
          </h2>
          <div className="space-y-3">
            {duplicates.map((group, i) => (
              <div
                key={i}
                className="rounded-xl p-4"
                style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}
              >
                <div className="flex items-center gap-2 mb-3">
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                    group.match_type === "invoice_number"
                      ? "bg-red-500/10 text-red-400"
                      : "bg-amber-500/10 text-amber-400"
                  }`}>
                    {group.match_type === "invoice_number" ? "Same Invoice #" : "Same Vendor + Amount + Date"}
                  </span>
                </div>
                <div className="space-y-2">
                  {group.invoices.map((inv) => (
                    <div key={inv.id} className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-3">
                        <Link href={`/invoices/${inv.id}`} className="text-blue-500 hover:text-blue-400 font-medium">
                          {inv.vendor_name || inv.file_name}
                        </Link>
                        <span style={{ color: "var(--text-muted)" }}>{inv.invoice_number || "---"}</span>
                      </div>
                      <div className="flex items-center gap-4">
                        <span className="font-medium" style={{ color: "var(--text-primary)" }}>
                          {inv.total_amount ? formatCurrency(inv.total_amount) : "---"}
                        </span>
                        <span className="text-xs" style={{ color: "var(--text-muted)" }}>{inv.status}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div>
        <h2 className="text-lg font-semibold mb-4" style={{ color: "var(--text-primary)" }}>Recent Invoices</h2>
        <InvoiceTable invoices={recent} showViewAll={invoices.length > 10} />
      </div>
    </div>
  );
}
