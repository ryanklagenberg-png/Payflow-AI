"use client";

import { useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import "react-pdf/dist/Page/AnnotationLayer.css";
import "react-pdf/dist/Page/TextLayer.css";

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

interface Props {
  url: string;
}

export default function PdfViewer({ url }: Props) {
  const [numPages, setNumPages] = useState(0);
  const [loadError, setLoadError] = useState(false);

  if (loadError) {
    return (
      <div className="w-full h-full flex items-center justify-center">
        <div className="text-center">
          <p style={{ color: "var(--text-secondary)" }}>Unable to display PDF</p>
          <a href={url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:text-blue-400 text-sm mt-2 inline-block">
            Download instead
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full h-full overflow-auto flex flex-col items-center py-4 gap-4" style={{ background: "#1a1a1a" }}>
      <Document
        file={url}
        onLoadSuccess={({ numPages }) => setNumPages(numPages)}
        onLoadError={() => setLoadError(true)}
        loading={
          <div className="flex items-center justify-center h-32">
            <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
          </div>
        }
      >
        {Array.from({ length: numPages }, (_, i) => (
          <Page
            key={i + 1}
            pageNumber={i + 1}
            width={500}
            className="shadow-lg mb-4"
          />
        ))}
      </Document>
    </div>
  );
}
