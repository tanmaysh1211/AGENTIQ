"use client";
import { useEffect, useRef } from "react";

interface ReasoningStreamProps {
  thoughts: string[];
  isActive: boolean;
}

export default function ReasoningStream({ thoughts, isActive }: ReasoningStreamProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [thoughts]);

  if (thoughts.length === 0 && !isActive) return null;

  return (
    <div style={{
      background: "#111127",
      border: "1px solid #2a2a4a",
      borderRadius: 16,
      padding: 24,
      marginBottom: 24
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 16 }}>
        <span style={{ fontSize: 18 }}>🧠</span>
        <h2 style={{ color: "#fff", fontSize: 18, fontWeight: 600 }}>Agent Reasoning</h2>
        {isActive && (
          <span style={{
            marginLeft: "auto", background: "#1a1a3a", color: "#6366f1",
            border: "1px solid #6366f1", borderRadius: 999,
            padding: "2px 10px", fontSize: 11
          }}>● Live</span>
        )}
      </div>
      <div style={{
        background: "#0a0a1f",
        borderRadius: 12,
        padding: 16,
        maxHeight: 256,
        overflowY: "auto"
      }}>
        <p style={{
          color: "#a0aec0", fontSize: 13, lineHeight: 1.7,
          fontFamily: "monospace", whiteSpace: "pre-wrap"
        }}>
          {thoughts.join("")}
          {isActive && <span style={{ borderRight: "2px solid #6366f1" }}> </span>}
        </p>
        <div ref={bottomRef} />
      </div>
    </div>
  );
}