export default function ConfidenceMeter({ score }: { score: number | null }) {
  if (score === null) return <span style={{ color: "var(--text-muted)" }}>—</span>;

  const pct = Math.round(score * 100);
  const color =
    pct >= 90 ? "bg-green-500" : pct >= 70 ? "bg-amber-500" : "bg-red-500";

  return (
    <div className="flex items-center gap-3">
      <div className="flex-1 h-2 rounded-full overflow-hidden" style={{ background: "var(--border)" }}>
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-sm font-medium" style={{ color: "var(--text-secondary)" }}>{pct}%</span>
    </div>
  );
}
