"use client";
import { useState } from "react";

interface LeadFormProps {
  onLeadCreated: () => void;
}

export default function LeadForm({ onLeadCreated }: LeadFormProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    name: "",
    company: "",
    email: "",
    phone: "",
    status: "New",
    description: "",
    deal_name: "",
    deal_amount: "",
    deal_stage: "Prospecting"
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    if (!form.name || !form.company) {
      alert("Name and Company are required!");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/leads", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          deal_amount: parseInt(form.deal_amount) || 0
        })
      });
      const data = await res.json();
      if (data.success) {
        setForm({
          name: "", company: "", email: "", phone: "",
          status: "New", description: "", deal_name: "",
          deal_amount: "", deal_stage: "Prospecting"
        });
        setIsOpen(false);
        onLeadCreated();
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const inputStyle = {
    width: "100%",
    background: "#0a0a1f",
    border: "1px solid #2a2a4a",
    borderRadius: 8,
    padding: "10px 12px",
    color: "#fff",
    fontSize: 14,
    outline: "none",
    marginTop: 4
  };

  const labelStyle = {
    color: "#888",
    fontSize: 12,
    fontWeight: 500
  };

  return (
    <div>
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          background: "#6366f1",
          color: "#fff",
          border: "none",
          borderRadius: 10,
          padding: "10px 20px",
          fontWeight: 600,
          fontSize: 14,
          cursor: "pointer",
          marginBottom: 16
        }}
      >
        + Add New Lead
      </button>

      {isOpen && (
        <div style={{
          background: "#111127",
          border: "1px solid #2a2a4a",
          borderRadius: 16,
          padding: 24,
          marginBottom: 24
        }}>
          <h3 style={{ color: "#fff", fontSize: 16, fontWeight: 600, marginBottom: 20 }}>
            New Lead Details
          </h3>

          {/* Row 1 */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
            <div>
              <label style={labelStyle}>Full Name *</label>
              <input name="name" value={form.name} onChange={handleChange}
                placeholder="Rahul Mehta" style={inputStyle} />
            </div>
            <div>
              <label style={labelStyle}>Company *</label>
              <input name="company" value={form.company} onChange={handleChange}
                placeholder="TechCorp India" style={inputStyle} />
            </div>
          </div>

          {/* Row 2 */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
            <div>
              <label style={labelStyle}>Email</label>
              <input name="email" value={form.email} onChange={handleChange}
                placeholder="rahul@techcorp.com" style={inputStyle} />
            </div>
            <div>
              <label style={labelStyle}>Phone</label>
              <input name="phone" value={form.phone} onChange={handleChange}
                placeholder="+91-9876543210" style={inputStyle} />
            </div>
          </div>

          {/* Row 3 */}
          <div style={{ marginBottom: 16 }}>
            <label style={labelStyle}>Description / Needs</label>
            <textarea name="description" value={form.description} onChange={handleChange}
              placeholder="What does this lead need? e.g. Enterprise AI solutions for automation"
              rows={3}
              style={{ ...inputStyle, resize: "none" as const }} />
          </div>

          {/* Row 4 */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16, marginBottom: 20 }}>
            <div>
              <label style={labelStyle}>Deal Name</label>
              <input name="deal_name" value={form.deal_name} onChange={handleChange}
                placeholder="Enterprise Deal" style={inputStyle} />
            </div>
            <div>
              <label style={labelStyle}>Deal Amount ($)</label>
              <input name="deal_amount" value={form.deal_amount} onChange={handleChange}
                placeholder="50000" type="number" style={inputStyle} />
            </div>
            <div>
              <label style={labelStyle}>Deal Stage</label>
              <select name="deal_stage" value={form.deal_stage} onChange={handleChange}
                style={inputStyle}>
                <option>Prospecting</option>
                <option>Qualification</option>
                <option>Proposal</option>
                <option>Negotiation</option>
                <option>Closed Won</option>
              </select>
            </div>
          </div>

          {/* Buttons */}
          <div style={{ display: "flex", gap: 12 }}>
            <button
              onClick={handleSubmit}
              disabled={loading}
              style={{
                background: "#6366f1",
                color: "#fff",
                border: "none",
                borderRadius: 10,
                padding: "10px 24px",
                fontWeight: 600,
                cursor: loading ? "not-allowed" : "pointer",
                opacity: loading ? 0.7 : 1
              }}
            >
              {loading ? "Saving..." : "Save Lead"}
            </button>
            <button
              onClick={() => setIsOpen(false)}
              style={{
                background: "transparent",
                color: "#888",
                border: "1px solid #2a2a4a",
                borderRadius: 10,
                padding: "10px 24px",
                cursor: "pointer"
              }}
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}