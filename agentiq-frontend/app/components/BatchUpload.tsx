"use client";
import { useState } from "react";

export default function BatchUpload() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/api/batch/process-csv", {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: "Failed to process CSV" });
    } finally {
      setLoading(false);
    }
  };

  const handleProcessAll = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch("http://localhost:8000/api/batch/process-all", {
        method: "POST"
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: "Failed to process all leads" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      background: "#111127",
      border: "1px solid #2a2a4a",
      borderRadius: 16,
      padding: 24,
      marginTop: 24
    }}>
      <h3 style={{ color: "#fff", fontSize: 16, fontWeight: 600, marginBottom: 8 }}>
        📦 Batch Processing
      </h3>
      <p style={{ color: "#666", fontSize: 13, marginBottom: 20 }}>
        Generate proposals for multiple leads simultaneously
      </p>

      <div style={{ display: "flex", gap: 12, marginBottom: 20, flexWrap: "wrap" as const }}>
        {/* CSV Upload */}
        <label style={{
          background: "#1a1a3a",
          border: "1px dashed #6366f1",
          borderRadius: 10,
          padding: "12px 20px",
          cursor: "pointer",
          color: "#6366f1",
          fontSize: 14,
          fontWeight: 600
        }}>
          {loading ? "Processing..." : "📄 Upload CSV"}
          <input
            type="file"
            accept=".csv"
            onChange={handleUpload}
            disabled={loading}
            style={{ display: "none" }}
          />
        </label>

        {/* Process All */}
        <button
          onClick={handleProcessAll}
          disabled={loading}
          style={{
            background: "#1a3a1a",
            border: "1px solid #166534",
            color: "#4ade80",
            borderRadius: 10,
            padding: "12px 20px",
            fontSize: 14,
            fontWeight: 600,
            cursor: loading ? "not-allowed" : "pointer",
            opacity: loading ? 0.7 : 1
          }}
        >
          {loading ? "Processing..." : "⚡ Process All Leads"}
        </button>
      </div>

      {/* CSV format hint */}
      <div style={{
        background: "#0a0a1f",
        borderRadius: 8,
        padding: 12,
        marginBottom: 16,
        fontFamily: "monospace",
        fontSize: 12,
        color: "#555"
      }}>
        CSV format: lead_id column required<br />
        LEAD_001<br />
        LEAD_002<br />
        LEAD_003
      </div>

      {/* Results */}
      {result && (
        <div style={{
          background: "#0a0a1f",
          borderRadius: 10,
          padding: 16
        }}>
          {result.error ? (
            <p style={{ color: "#ef4444" }}>❌ {result.error}</p>
          ) : (
            <>
              <div style={{ display: "flex", gap: 24, marginBottom: 12 }}>
                <span style={{ color: "#fff" }}>Total: <b>{result.total}</b></span>
                <span style={{ color: "#4ade80" }}>✅ Success: <b>{result.success}</b></span>
                <span style={{ color: "#ef4444" }}>❌ Failed: <b>{result.failed || 0}</b></span>
              </div>
              {result.results?.map((r: any) => (
                <div key={r.lead_id} style={{
                  display: "flex", gap: 12,
                  padding: "6px 0",
                  borderBottom: "1px solid #1a1a2a",
                  fontSize: 13
                }}>
                  <span style={{ color: "#888" }}>{r.lead_id}</span>
                  <span style={{
                    color: r.status === "success" ? "#4ade80" : "#ef4444"
                  }}>
                    {r.status === "success" ? "✅ Done" : `❌ ${r.error}`}
                  </span>
                </div>
              ))}
            </>
          )}
        </div>
      )}
    </div>
  );
}