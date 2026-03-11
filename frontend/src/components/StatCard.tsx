import Link from "next/link";

interface StatCardProps {
  label: string;
  value: string;
  icon: string;
  color: string;
  href?: string;
}

export default function StatCard({ label, value, icon, color, href }: StatCardProps) {
  const content = (
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm" style={{ color: "var(--text-secondary)" }}>{label}</p>
        <p className="text-2xl font-bold mt-1" style={{ color: "var(--text-primary)" }}>{value}</p>
      </div>
      <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${color}`}>
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
          <path strokeLinecap="round" strokeLinejoin="round" d={icon} />
        </svg>
      </div>
    </div>
  );

  if (href) {
    return (
      <Link
        href={href}
        className="rounded-xl p-6 block transition-colors hover:brightness-110"
        style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}
      >
        {content}
      </Link>
    );
  }

  return (
    <div className="rounded-xl p-6" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
      {content}
    </div>
  );
}
