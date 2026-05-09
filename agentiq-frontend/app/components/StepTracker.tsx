"use client";

interface Step {
  id: string;
  label: string;
  sublabel: string;
  status: "pending" | "active" | "done";
}

export default function StepTracker({ steps }: { steps: Step[] }) {
  return (
    <div style={{
      background: "#111127",
      border: "1px solid #2a2a4a",
      borderRadius: 16,
      padding: 24,
      marginBottom: 24
    }}>
      <h2 style={{ color: "#fff", fontSize: 18, fontWeight: 600, marginBottom: 20 }}>
        Agent Progress
      </h2>
      {steps.map((step, i) => (
        <div key={step.id} style={{ display: "flex", alignItems: "flex-start", gap: 16, marginBottom: i < steps.length - 1 ? 24 : 0 }}>
          {/* Icon */}
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <div style={{
              width: 40, height: 40, borderRadius: "50%",
              display: "flex", alignItems: "center", justifyContent: "center",
              border: `2px solid ${step.status === "pending" ? "#2a2a4a" : "#6366f1"}`,
              background: step.status === "done" ? "#6366f1" : "transparent",
              fontSize: 16, flexShrink: 0
            }}>
              {step.status === "done" ? "✓" : step.status === "active" ? "⏳" : "○"}
            </div>
            {i < steps.length - 1 && (
              <div style={{
                width: 2, height: 28, marginTop: 4,
                background: step.status === "done" ? "#6366f1" : "#2a2a4a"
              }} />
            )}
          </div>
          {/* Text */}
          <div style={{ paddingTop: 8, flex: 1 }}>
            <p style={{
              color: step.status === "pending" ? "#666" : step.status === "active" ? "#6366f1" : "#fff",
              fontWeight: 500, fontSize: 15, marginBottom: 2
            }}>
              {step.label}
            </p>
            <p style={{ color: "#555", fontSize: 12 }}>{step.sublabel}</p>
          </div>
          {/* Badge */}
          <div style={{ paddingTop: 8 }}>
            {step.status === "done" && (
              <span style={{
                background: "#1a3a1a", color: "#4ade80",
                border: "1px solid #166534", borderRadius: 999,
                padding: "2px 10px", fontSize: 11
              }}>Done</span>
            )}
            {step.status === "active" && (
              <span style={{
                background: "#1a1a3a", color: "#6366f1",
                border: "1px solid #6366f1", borderRadius: 999,
                padding: "2px 10px", fontSize: 11
              }}>Running</span>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}