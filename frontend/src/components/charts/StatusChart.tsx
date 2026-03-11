"use client";

import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from "recharts";

const STATUS_COLORS: Record<string, string> = {
  extracted: "#3b82f6",
  approved: "#10b981",
  rejected: "#ef4444",
  failed: "#f87171",
  uploaded: "#64748b",
  processing: "#f59e0b",
};

interface Props {
  data: { name: string; value: number }[];
}

export default function StatusChart({ data }: Props) {
  if (data.length === 0) {
    return <p className="text-sm text-center py-8" style={{ color: "var(--text-muted)" }}>No data</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={200}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={50}
          outerRadius={80}
          paddingAngle={2}
          dataKey="value"
        >
          {data.map((entry, i) => (
            <Cell key={i} fill={STATUS_COLORS[entry.name] || "#64748b"} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            background: "#1e293b",
            border: "1px solid #334155",
            borderRadius: "8px",
            color: "#e2e8f0",
          }}
          formatter={(value: unknown, name: unknown) => [String(value), String(name).charAt(0).toUpperCase() + String(name).slice(1)]}
        />
        <Legend
          formatter={(value: string) => (
            <span style={{ color: "var(--text-secondary)", fontSize: "12px", textTransform: "capitalize" }}>
              {value}
            </span>
          )}
        />
      </PieChart>
    </ResponsiveContainer>
  );
}
