"use client";

import { Suspense, useEffect, useState, useCallback } from "react";
import { useSearchParams } from "next/navigation";
import { fetchInvoices, getExportCsvUrl } from "@/lib/api";
import { InvoiceListItem } from "@/lib/types";
import InvoiceTable from "@/components/InvoiceTable";

const STATUSES = ["all", "extracted", "approved", "rejected", "processing", "uploaded", "failed"];
const PAGE_SIZE = 25;

export default function InvoicesPage() {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
    }>
      <InvoicesContent />
    </Suspense>
  );
}

function InvoicesContent() {
  const searchParams = useSearchParams();
  const initialStatus = searchParams.get("status") || "all";
  const [invoices, setInvoices] = useState<InvoiceListItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState(initialStatus);
  const [search, setSearch] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [jobNumberFilter, setJobNumberFilter] = useState("");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [showFilters, setShowFilters] = useState(false);
  const [page, setPage] = useState(1);

  const loadInvoices = useCallback(() => {
    setLoading(true);
    fetchInvoices({
      status: statusFilter === "all" ? undefined : statusFilter,
      limit: PAGE_SIZE,
      skip: (page - 1) * PAGE_SIZE,
      search: searchQuery || undefined,
      job_number: jobNumberFilter || undefined,
    })
      .then(({ items, total: t }) => {
        setInvoices(items);
        setTotal(t);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [statusFilter, page, searchQuery, jobNumberFilter]);

  useEffect(() => {
    loadInvoices();
  }, [loadInvoices]);

  // Reset page when filters change
  useEffect(() => {
    setPage(1);
  }, [statusFilter, searchQuery, jobNumberFilter]);

  const handleSearchSubmit = () => {
    setSearchQuery(search);
  };

  const handleSearchKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSearchSubmit();
    }
  };

  const filtered = invoices.filter((inv) => {
    if (dateFrom && inv.invoice_date) {
      if (inv.invoice_date < dateFrom) return false;
    }
    if (dateTo && inv.invoice_date) {
      if (inv.invoice_date > dateTo) return false;
    }
    if ((dateFrom || dateTo) && !inv.invoice_date) return false;
    return true;
  });

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  const startItem = (page - 1) * PAGE_SIZE + 1;
  const endItem = Math.min(page * PAGE_SIZE, total);

  const activeFilterCount = (dateFrom ? 1 : 0) + (dateTo ? 1 : 0) + (jobNumberFilter ? 1 : 0);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold" style={{ color: "var(--text-primary)" }}>Invoices</h1>
          <p className="text-sm mt-1" style={{ color: "var(--text-secondary)" }}>All processed invoices</p>
        </div>
        <a
          href={getExportCsvUrl(statusFilter === "all" ? undefined : statusFilter)}
          download
          className="px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
          </svg>
          Export CSV
        </a>
      </div>

      <div className="space-y-3">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="flex-1 relative">
            <input
              type="text"
              placeholder="Search by vendor, invoice #, or file name..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={handleSearchKeyDown}
              className="w-full rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500"
              style={{ background: "var(--bg-input)", border: "1px solid var(--border)", color: "var(--text-primary)" }}
            />
            {search && (
              <button
                onClick={() => { setSearch(""); setSearchQuery(""); }}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-xs"
                style={{ color: "var(--text-muted)" }}
              >
                ✕
              </button>
            )}
          </div>
          <button
            onClick={handleSearchSubmit}
            className="px-4 py-2.5 rounded-lg text-sm font-medium bg-blue-600 hover:bg-blue-500 text-white transition-colors"
          >
            Search
          </button>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`px-4 py-2.5 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 ${
              showFilters || activeFilterCount > 0 ? "bg-blue-600 text-white" : ""
            }`}
            style={!showFilters && activeFilterCount === 0 ? { background: "var(--bg-input)", border: "1px solid var(--border)", color: "var(--text-secondary)" } : undefined}
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 01-.659 1.591l-5.432 5.432a2.25 2.25 0 00-.659 1.591v2.927a2.25 2.25 0 01-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 00-.659-1.591L3.659 7.409A2.25 2.25 0 013 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0112 3z" />
            </svg>
            Filters{activeFilterCount > 0 ? ` (${activeFilterCount})` : ""}
          </button>
        </div>

        {/* Expandable filter panel */}
        {showFilters && (
          <div className="rounded-xl p-4 space-y-4" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <div className="flex flex-wrap gap-4">
              <div>
                <label className="text-xs uppercase tracking-wider block mb-1.5" style={{ color: "var(--text-muted)" }}>Job Number</label>
                <input
                  type="text"
                  placeholder="Filter by job #..."
                  value={jobNumberFilter}
                  onChange={(e) => setJobNumberFilter(e.target.value)}
                  className="rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                  style={{ background: "var(--bg-input)", border: "1px solid var(--border)", color: "var(--text-primary)" }}
                />
              </div>
              <div>
                <label className="text-xs uppercase tracking-wider block mb-1.5" style={{ color: "var(--text-muted)" }}>Date From</label>
                <input
                  type="date"
                  value={dateFrom}
                  onChange={(e) => setDateFrom(e.target.value)}
                  className="rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                  style={{ background: "var(--bg-input)", border: "1px solid var(--border)", color: "var(--text-primary)" }}
                />
              </div>
              <div>
                <label className="text-xs uppercase tracking-wider block mb-1.5" style={{ color: "var(--text-muted)" }}>Date To</label>
                <input
                  type="date"
                  value={dateTo}
                  onChange={(e) => setDateTo(e.target.value)}
                  className="rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                  style={{ background: "var(--bg-input)", border: "1px solid var(--border)", color: "var(--text-primary)" }}
                />
              </div>
            </div>
            {activeFilterCount > 0 && (
              <button
                onClick={() => { setDateFrom(""); setDateTo(""); setJobNumberFilter(""); }}
                className="text-xs text-blue-500 hover:text-blue-400"
              >
                Clear all filters
              </button>
            )}
          </div>
        )}

        {/* Status tabs */}
        <div className="flex gap-1 rounded-lg p-1" style={{ background: "var(--bg-input)", border: "1px solid var(--border)" }}>
          {STATUSES.map((s) => (
            <button
              key={s}
              onClick={() => setStatusFilter(s)}
              className={`px-3 py-1.5 rounded-md text-xs font-medium capitalize transition-colors ${
                statusFilter === s ? "bg-blue-600 text-white" : ""
              }`}
              style={statusFilter !== s ? { color: "var(--text-secondary)" } : undefined}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      {/* Results count */}
      {!loading && (
        <p className="text-xs" style={{ color: "var(--text-muted)" }}>
          Showing {total > 0 ? `${startItem}-${endItem}` : "0"} of {total} invoice{total !== 1 ? "s" : ""}{searchQuery || jobNumberFilter || dateFrom || dateTo || statusFilter !== "all" ? " matching filters" : ""}
        </p>
      )}

      {loading ? (
        <div className="flex items-center justify-center h-32">
          <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <>
          <InvoiceTable invoices={filtered} />

          {/* Pagination controls */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between pt-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page <= 1}
                className="px-4 py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-40"
                style={{ background: "var(--bg-input)", border: "1px solid var(--border)", color: "var(--text-secondary)" }}
              >
                Previous
              </button>
              <span className="text-sm" style={{ color: "var(--text-secondary)" }}>
                Page {page} of {totalPages}
              </span>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page >= totalPages}
                className="px-4 py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-40"
                style={{ background: "var(--bg-input)", border: "1px solid var(--border)", color: "var(--text-secondary)" }}
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
