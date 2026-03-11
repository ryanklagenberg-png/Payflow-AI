const statusConfig: Record<string, { bg: string; text: string; label: string }> = {
  uploaded: { bg: "bg-slate-500/10", text: "text-slate-400", label: "Uploaded" },
  processing: { bg: "bg-amber-500/10", text: "text-amber-400", label: "Processing" },
  extracted: { bg: "bg-green-500/10", text: "text-green-400", label: "Extracted" },
  approved: { bg: "bg-emerald-500/10", text: "text-emerald-400", label: "Approved" },
  rejected: { bg: "bg-red-500/10", text: "text-red-400", label: "Rejected" },
  failed: { bg: "bg-red-500/10", text: "text-red-400", label: "Failed" },
};

export default function StatusBadge({ status }: { status: string }) {
  const config = statusConfig[status] || statusConfig.uploaded;
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.bg} ${config.text}`}>
      {config.label}
    </span>
  );
}
