"use client";
import { useState } from "react";

export default function DownloadButton({ show, leadId }: { show: boolean; leadId: string }) {
  const [downloading, setDownloading] = useState(false);
  const [downloaded, setDownloaded] = useState(false);

  if (!show) return null;

  const handleDownload = async () => {
    setDownloading(true);
    try {
      const res = await fetch("http://localhost:8000/api/agent/export-pdf", { method: "POST" });
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `proposal_${leadId}.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
      setDownloaded(true);
      setTimeout(() => setDownloaded(false), 3000);
    } catch (e) {
      console.error(e);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div style={{
      background: "linear-gradient(135deg, #1a1a3a, #111127)",
      border: "1px solid #6366f1",
      borderRadius: 16,
      padding: 32,
      textAlign: "center"
    }}>
      <div style={{ fontSize: 40, marginBottom: 12 }}>✅</div>
      <h3 style={{ color: "#fff", fontSize: 20, fontWeight: 600, marginBottom: 8 }}>
        Proposal Ready!
      </h3>
      <p style={{ color: "#888", fontSize: 14, marginBottom: 24 }}>
        AI-generated sales proposal for {leadId}
      </p>
      <button
        onClick={handleDownload}
        disabled={downloading}
        style={{
          background: "#6366f1",
          color: "#fff",
          border: "none",
          borderRadius: 12,
          padding: "14px 32px",
          fontWeight: 600,
          fontSize: 15,
          cursor: downloading ? "not-allowed" : "pointer",
          opacity: downloading ? 0.7 : 1
        }}
      >
        {downloading ? "Downloading..." : downloaded ? "Downloaded! ✓" : "📄 Download PDF Proposal"}
      </button>
    </div>
  );
}