"use client";

import { useCallback, useState } from "react";
import { useRouter } from "next/navigation";
import { uploadInvoice } from "@/lib/api";
import { UploadResponse } from "@/lib/types";

const ALLOWED_TYPES = ["application/pdf", "image/png", "image/jpeg", "image/webp", "image/tiff"];
const MAX_SIZE_MB = 20;

interface FileEntry {
  file: File;
  status: "pending" | "uploading" | "done" | "error";
  result?: UploadResponse;
  error?: string;
}

export default function UploadZone() {
  const router = useRouter();
  const [files, setFiles] = useState<FileEntry[]>([]);
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);

  const validateFile = (f: File): string | null => {
    if (!ALLOWED_TYPES.includes(f.type)) return "File type not supported.";
    if (f.size > MAX_SIZE_MB * 1024 * 1024) return `File exceeds ${MAX_SIZE_MB}MB limit.`;
    return null;
  };

  const addFiles = (newFiles: FileList | File[]) => {
    const entries: FileEntry[] = [];
    for (const f of Array.from(newFiles)) {
      const err = validateFile(f);
      if (err) {
        entries.push({ file: f, status: "error", error: err });
      } else {
        entries.push({ file: f, status: "pending" });
      }
    }
    setFiles((prev) => [...prev, ...entries]);
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    if (e.dataTransfer.files.length > 0) addFiles(e.dataTransfer.files);
  }, []);

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    const pending = files.filter((f) => f.status === "pending");
    if (pending.length === 0) return;
    setUploading(true);

    for (let i = 0; i < files.length; i++) {
      if (files[i].status !== "pending") continue;

      setFiles((prev) =>
        prev.map((f, idx) => (idx === i ? { ...f, status: "uploading" } : f))
      );

      try {
        const result = await uploadInvoice(files[i].file);
        setFiles((prev) =>
          prev.map((f, idx) => (idx === i ? { ...f, status: "done", result } : f))
        );
      } catch {
        setFiles((prev) =>
          prev.map((f, idx) => (idx === i ? { ...f, status: "error", error: "Upload failed" } : f))
        );
      }
    }

    setUploading(false);
  };

  const pendingCount = files.filter((f) => f.status === "pending").length;
  const doneCount = files.filter((f) => f.status === "done").length;

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-xl p-16 text-center transition-colors cursor-pointer ${
          dragging ? "border-blue-500 bg-blue-500/5" : ""
        }`}
        style={!dragging ? { borderColor: "var(--border)", background: "var(--bg-card)" } : undefined}
        onClick={() => document.getElementById("file-input")?.click()}
      >
        <input
          id="file-input"
          type="file"
          accept=".pdf,.png,.jpg,.jpeg,.webp,.tiff"
          multiple
          className="hidden"
          onChange={(e) => {
            if (e.target.files && e.target.files.length > 0) addFiles(e.target.files);
            e.target.value = "";
          }}
        />

        <svg className="w-16 h-16 mx-auto" style={{ color: "var(--text-muted)" }} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
        </svg>

        <p className="mt-4 text-lg" style={{ color: "var(--text-primary)" }}>
          Drop invoices here or click to browse
        </p>
        <p className="text-sm mt-2" style={{ color: "var(--text-muted)" }}>
          PDF, PNG, JPG, WEBP, or TIFF — up to 20MB each — multiple files supported
        </p>
      </div>

      {/* File List */}
      {files.length > 0 && (
        <div className="rounded-xl overflow-hidden" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
          {files.map((entry, i) => (
            <div
              key={`${entry.file.name}-${i}`}
              className="flex items-center justify-between px-4 py-3"
              style={{ borderBottom: i < files.length - 1 ? "1px solid var(--border)" : undefined }}
            >
              <div className="flex items-center gap-3 min-w-0 flex-1">
                {entry.status === "uploading" && (
                  <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin flex-shrink-0" />
                )}
                {entry.status === "done" && (
                  <svg className="w-4 h-4 text-green-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                )}
                {entry.status === "error" && (
                  <svg className="w-4 h-4 text-red-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                )}
                {entry.status === "pending" && (
                  <svg className="w-4 h-4 text-blue-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                )}

                <span className="text-sm truncate" style={{ color: "var(--text-primary)" }}>{entry.file.name}</span>
                <span className="text-xs flex-shrink-0" style={{ color: "var(--text-muted)" }}>
                  ({(entry.file.size / 1024 / 1024).toFixed(1)} MB)
                </span>
              </div>

              <div className="flex items-center gap-3 flex-shrink-0 ml-3">
                {entry.status === "done" && entry.result && (
                  <button
                    onClick={() => router.push(`/invoices/${entry.result!.id}`)}
                    className="text-xs text-blue-500 hover:text-blue-400"
                  >
                    View
                  </button>
                )}
                {entry.error && (
                  <span className="text-xs text-red-400">{entry.error}</span>
                )}
                {entry.status === "uploading" && (
                  <span className="text-xs text-blue-400">Processing...</span>
                )}
                {(entry.status === "pending" || entry.status === "error") && !uploading && (
                  <button
                    onClick={() => removeFile(i)}
                    className="text-xs hover:text-red-400 transition-colors"
                    style={{ color: "var(--text-muted)" }}
                  >
                    Remove
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Actions */}
      {files.length > 0 && !uploading && (
        <div className="flex items-center justify-between">
          <div className="flex gap-3">
            {pendingCount > 0 && (
              <button
                onClick={handleUpload}
                className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                Upload & Extract {pendingCount > 1 ? `(${pendingCount} files)` : ""}
              </button>
            )}
            {doneCount > 0 && pendingCount === 0 && (
              <button
                onClick={() => router.push("/invoices")}
                className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                View All Invoices
              </button>
            )}
          </div>
          <button
            onClick={() => setFiles([])}
            className="text-sm hover:text-red-400 transition-colors"
            style={{ color: "var(--text-muted)" }}
          >
            Clear all
          </button>
        </div>
      )}

      {uploading && (
        <div className="flex items-center justify-center gap-3 py-2">
          <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
          <span className="text-sm text-blue-500">Processing invoices with AI...</span>
        </div>
      )}
    </div>
  );
}
