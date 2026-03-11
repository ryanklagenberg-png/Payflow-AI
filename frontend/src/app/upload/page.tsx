import UploadZone from "@/components/UploadZone";

export default function UploadPage() {
  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-2xl font-bold" style={{ color: "var(--text-primary)" }}>Upload Invoice</h1>
        <p className="text-sm mt-1" style={{ color: "var(--text-secondary)" }}>
          Upload a construction invoice and AI will extract all the data automatically
        </p>
      </div>

      <UploadZone />

      <div className="rounded-xl p-6" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
        <h3 className="text-sm font-medium mb-3" style={{ color: "var(--text-primary)" }}>What gets extracted:</h3>
        <div className="grid grid-cols-2 gap-2 text-sm" style={{ color: "var(--text-secondary)" }}>
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
            Vendor name & address
          </div>
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
            Invoice number & dates
          </div>
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
            PO number
          </div>
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
            Line items with quantities
          </div>
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
            Subtotal, tax & total
          </div>
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
            Payment terms
          </div>
        </div>
      </div>
    </div>
  );
}
