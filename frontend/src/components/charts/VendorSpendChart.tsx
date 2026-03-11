"use client";

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

interface Props {
  data: { name: string; amount: number }[];
}

export default function VendorSpendChart({ data }: Props) {
  if (data.length === 0) {
    return <p className="text-sm text-center py-8" style={{ color: "var(--text-muted)" }}>No data</p>;
  }

  const formatted = data.map((d) => ({
    ...d,
    name: d.name.length > 15 ? d.name.slice(0, 15) + "..." : d.name,
  }));

  return (
    <ResponsiveContainer width="100%" height={200}>
      <BarChart data={formatted} layout="vertical" margin={{ left: 0, right: 10 }}>
        <XAxis
          type="number"
          tick={{ fill: "var(--text-muted)", fontSize: 11 }}
          tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
          axisLine={false}
          tickLine={false}
        />
        <YAxis
          type="category"
          dataKey="name"
          width={110}
          tick={{ fill: "var(--text-secondary)", fontSize: 11 }}
          axisLine={false}
          tickLine={false}
        />
        <Tooltip
          contentStyle={{
            background: "#1e293b",
            border: "1px solid #334155",
            borderRadius: "8px",
            color: "#e2e8f0",
          }}
          formatter={(value: unknown) => [
            `$${Number(value).toLocaleString("en-US", { minimumFractionDigits: 2 })}`,
            "Spend",
          ]}
        />
        <Bar dataKey="amount" fill="#3b82f6" radius={[0, 4, 4, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
