"use client";

interface Lead {
  id: string;
  name: string;
  company: string;
  email: string;
  status: string;
  deal_amount: number;
  deal_stage: string;
  description: string;
}

interface LeadsListProps {
  leads: Lead[];
  onRunAgent: (leadId: string) => void;
  onDelete: (leadId: string) => void;
  isLoading: boolean;
  currentLeadId: string;
}

export default function LeadsList({
  leads, onRunAgent, onDelete, isLoading, currentLeadId
}: LeadsListProps) {

  const stageColor = (stage: string) => {
    const colors: Record<string, string> = {
      "Prospecting": "#f59e0b",
      "Qualification": "#3b82f6",
      "Proposal": "#8b5cf6",
      "Negotiation": "#f97316",
      "Closed Won": "#10b981"
    };
    return colors[stage] || "#6366f1";
  };

  if (leads.length === 0) {
    return (
      <div style={{ textAlign: "center", padding: "40px 0", color: "#555" }}>
        <div style={{ fontSize: 40, marginBottom: 8 }}>📋</div>
        <p>No leads yet. Add your first lead above!</p>
      </div>
    );
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
      {leads.map((lead) => (
        <div
          key={lead.id}
          style={{
            background: "#0d0d1f",
            border: currentLeadId === lead.id ? "1px solid #6366f1" : "1px solid #2a2a4a",
            borderRadius: 12,
            padding: 16,
            display: "flex",
            alignItems: "center",
            gap: 16,
            transition: "border 0.2s"
          }}
        >
          {/* Avatar */}
          <div style={{
            width: 44, height: 44,
            background: "#1a1a3a",
            borderRadius: "50%",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 18, flexShrink: 0
          }}>
            {lead.name.charAt(0)}
          </div>

          {/* Info */}
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
              <span style={{ color: "#fff", fontWeight: 600, fontSize: 15 }}>
                {lead.name}
              </span>
              <span style={{ color: "#555", fontSize: 12 }}>•</span>
              <span style={{ color: "#888", fontSize: 13 }}>{lead.company}</span>
              <span style={{
                marginLeft: "auto",
                background: "#1a1a2a",
                color: stageColor(lead.deal_stage),
                border: `1px solid ${stageColor(lead.deal_stage)}`,
                borderRadius: 999,
                padding: "2px 8px",
                fontSize: 11
              }}>
                {lead.deal_stage}
              </span>
            </div>
            <div style={{ display: "flex", gap: 16 }}>
              <span style={{ color: "#555", fontSize: 12 }}>🆔 {lead.id}</span>
              <span style={{ color: "#555", fontSize: 12 }}>
                💰 ${lead.deal_amount?.toLocaleString()}
              </span>
              <span style={{ color: "#555", fontSize: 12, overflow: "hidden",
                textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: 200 }}>
                {lead.description}
              </span>
            </div>
          </div>

          {/* Actions */}
          <div style={{ display: "flex", gap: 8, flexShrink: 0 }}>
            <button
              onClick={() => onRunAgent(lead.id)}
              disabled={isLoading}
              style={{
                background: isLoading && currentLeadId === lead.id ? "#3a3a6a" : "#6366f1",
                color: "#fff",
                border: "none",
                borderRadius: 8,
                padding: "8px 16px",
                fontSize: 13,
                fontWeight: 600,
                cursor: isLoading ? "not-allowed" : "pointer",
                opacity: isLoading && currentLeadId !== lead.id ? 0.5 : 1
              }}
            >
              {isLoading && currentLeadId === lead.id ? "⏳ Running..." : "▶ Generate"}
            </button>
            <button
              onClick={() => onDelete(lead.id)}
              style={{
                background: "transparent",
                color: "#ef4444",
                border: "1px solid #3a1a1a",
                borderRadius: 8,
                padding: "8px 12px",
                fontSize: 13,
                cursor: "pointer"
              }}
            >
              🗑
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}