"use client";
import { useState } from "react";

interface LeadInputProps {
  onSubmit: (leadId: string) => void;
  isLoading: boolean;
}

export default function LeadInput({ onSubmit, isLoading }: LeadInputProps) {
  const [leadId, setLeadId] = useState("LEAD_001");

  return (
    <div style={{
      background: "#111127",
      border: "1px solid #2a2a4a",
      borderRadius: 16,
      padding: 24,
      marginBottom: 24
    }}>
      <h2 style={{ color: "#fff", fontSize: 18, fontWeight: 600, marginBottom: 16 }}>
        ⚡ Generate Sales Proposal
      </h2>
      <div style={{ display: "flex", gap: 12, marginBottom: 12 }}>
        <input
          type="text"
          value={leadId}
          onChange={(e) => setLeadId(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !isLoading && onSubmit(leadId)}
          placeholder="Enter Lead ID (e.g. LEAD_001)"
          disabled={isLoading}
          style={{
            flex: 1,
            background: "#0a0a1f",
            border: "1px solid #2a2a4a",
            borderRadius: 12,
            padding: "12px 16px",
            color: "#fff",
            fontSize: 14,
            outline: "none",
            opacity: isLoading ? 0.5 : 1
          }}
        />
        <button
          onClick={() => !isLoading && leadId && onSubmit(leadId)}
          disabled={isLoading || !leadId}
          style={{
            background: "#6366f1",
            color: "#fff",
            border: "none",
            borderRadius: 12,
            padding: "12px 24px",
            fontWeight: 600,
            cursor: isLoading ? "not-allowed" : "pointer",
            opacity: isLoading ? 0.6 : 1,
            fontSize: 14
          }}
        >
          {isLoading ? "Running..." : "🔍 Run Agent"}
        </button>
      </div>
      <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <span style={{ color: "#666", fontSize: 13 }}>Quick:</span>
        {["LEAD_001", "LEAD_002", "LEAD_003"].map((id) => (
          <button
            key={id}
            onClick={() => setLeadId(id)}
            disabled={isLoading}
            style={{
              background: "#1a1a3a",
              border: "1px solid #2a2a4a",
              color: "#6366f1",
              borderRadius: 8,
              padding: "4px 12px",
              fontSize: 12,
              cursor: "pointer"
            }}
          >
            {id}
          </button>
        ))}
      </div>
    </div>
  );
}