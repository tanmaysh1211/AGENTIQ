// "use client";
// import { useState, useCallback } from "react";
// import LeadInput from "./components/LeadInput";
// import StepTracker from "./components/StepTracker";
// import ReasoningStream from "./components/ReasoningStream";
// import DownloadButton from "./components/DownloadButton";

// interface Step {
//   id: string;
//   label: string;
//   sublabel: string;
//   status: "pending" | "active" | "done";
// }

// const INITIAL_STEPS: Step[] = [
//   { id: "crm_fetch_tool", label: "Fetching CRM Data", sublabel: "Retrieving lead info from Salesforce", status: "pending" },
//   { id: "rag_search_tool", label: "Searching Knowledge Base", sublabel: "Finding relevant products and pricing", status: "pending" },
//   { id: "pdf_generation_tool", label: "Generating PDF Proposal", sublabel: "Creating personalized proposal document", status: "pending" },
// ];

// export default function Home() {
//   const [isLoading, setIsLoading] = useState(false);
//   const [steps, setSteps] = useState<Step[]>(INITIAL_STEPS);
//   const [thoughts, setThoughts] = useState<string[]>([]);
//   const [isDone, setIsDone] = useState(false);
//   const [currentLeadId, setCurrentLeadId] = useState("");
//   const [isThinking, setIsThinking] = useState(false);

//   const updateStep = useCallback((toolName: string, status: "active" | "done") => {
//     setSteps((prev) => prev.map((s) => s.id === toolName ? { ...s, status } : s));
//   }, []);

//   const handleRunAgent = useCallback((leadId: string) => {
//     setIsLoading(true);
//     setIsDone(false);
//     setThoughts([]);
//     setIsThinking(false);
//     setCurrentLeadId(leadId);
//     setSteps(INITIAL_STEPS);

//     const eventSource = new EventSource(`http://localhost:8000/api/agent/stream/${leadId}`);

//     eventSource.addEventListener("tool_call", (e) => {
//       const data = JSON.parse(e.data);
//       updateStep(data.tool, "active");
//     });
//     eventSource.addEventListener("tool_result", (e) => {
//       const data = JSON.parse(e.data);
//       updateStep(data.tool, "done");
//     });
//     eventSource.addEventListener("thinking", (e) => {
//       const data = JSON.parse(e.data);
//       setIsThinking(true);
//       setThoughts((prev) => [...prev, data.content]);
//     });
//     eventSource.addEventListener("done", () => {
//       setIsDone(true);
//       setIsLoading(false);
//       setIsThinking(false);
//       eventSource.close();
//     });
//     eventSource.onerror = () => {
//       setIsLoading(false);
//       setIsThinking(false);
//       eventSource.close();
//     };
//   }, [updateStep]);

//   return (
//     <div style={{ minHeight: "100vh", background: "#0a0a0f", color: "#e2e8f0" }}>
//       {/* Header */}
//       <div style={{
//         borderBottom: "1px solid #2a2a4a",
//         background: "#0d0d1f",
//         padding: "16px 24px",
//         display: "flex",
//         alignItems: "center",
//         gap: 12
//       }}>
//         <div style={{
//           width: 36, height: 36, background: "#6366f1",
//           borderRadius: 10, display: "flex", alignItems: "center",
//           justifyContent: "center", fontSize: 18
//         }}>🤖</div>
//         <div>
//           <div style={{ color: "#fff", fontWeight: 700, fontSize: 18, lineHeight: 1 }}>AgentIQ</div>
//           <div style={{ color: "#666", fontSize: 12 }}>Agentic AI Sales Automation</div>
//         </div>
//         <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 6 }}>
//           <div style={{ width: 8, height: 8, background: "#4ade80", borderRadius: "50%" }} />
//           <span style={{ color: "#4ade80", fontSize: 12 }}>Backend Online</span>
//         </div>
//       </div>

//       {/* Content */}
//       <div style={{ maxWidth: 720, margin: "0 auto", padding: "32px 24px" }}>
//         <LeadInput onSubmit={handleRunAgent} isLoading={isLoading} />

//         {(isLoading || isDone) && (
//           <>
//             <StepTracker steps={steps} />
//             <ReasoningStream thoughts={thoughts} isActive={isThinking} />
//             <DownloadButton show={isDone} leadId={currentLeadId} />
//           </>
//         )}

//         {!isLoading && !isDone && (
//           <div style={{ textAlign: "center", paddingTop: 80 }}>
//             <div style={{
//               width: 64, height: 64, background: "#1a1a3a",
//               borderRadius: 16, display: "flex", alignItems: "center",
//               justifyContent: "center", margin: "0 auto 16px", fontSize: 32
//             }}>🤖</div>
//             <h3 style={{ color: "#fff", fontSize: 20, fontWeight: 600, marginBottom: 8 }}>
//               Ready to Generate Proposals
//             </h3>
//             <p style={{ color: "#666", fontSize: 14, maxWidth: 380, margin: "0 auto" }}>
//               Enter a Lead ID above and the AI agent will automatically fetch CRM data,
//               search the knowledge base, and generate a personalized PDF proposal.
//             </p>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }





"use client";
import { useState, useCallback, useEffect } from "react";
import LeadInput from "./components/LeadInput";
import StepTracker from "./components/StepTracker";
import ReasoningStream from "./components/ReasoningStream";
import DownloadButton from "./components/DownloadButton";
import LeadForm from "./components/LeadForm";
import LeadsList from "./components/LeadsList";
import BatchUpload from "./components/BatchUpload";

interface Step {
  id: string;
  label: string;
  sublabel: string;
  status: "pending" | "active" | "done";
}

const INITIAL_STEPS: Step[] = [
  { id: "crm_fetch_tool", label: "Fetching CRM Data", sublabel: "Retrieving lead info from Salesforce", status: "pending" },
  { id: "rag_search_tool", label: "Searching Knowledge Base", sublabel: "Finding relevant products and pricing", status: "pending" },
  { id: "pdf_generation_tool", label: "Generating PDF Proposal", sublabel: "Creating personalized proposal document", status: "pending" },
];

export default function Home() {
  const [activeTab, setActiveTab] = useState<"generate" | "leads" | "batch">("generate");
  const [isLoading, setIsLoading] = useState(false);
  const [steps, setSteps] = useState<Step[]>(INITIAL_STEPS);
  const [thoughts, setThoughts] = useState<string[]>([]);
  const [isDone, setIsDone] = useState(false);
  const [currentLeadId, setCurrentLeadId] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const [leads, setLeads] = useState<any[]>([]);
  const [leadsLoading, setLeadsLoading] = useState(false);

  const fetchLeads = async () => {
    setLeadsLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/leads");
      const data = await res.json();
      setLeads(data.leads || []);
    } catch (e) {
      console.error("Failed to fetch leads:", e);
    } finally {
      setLeadsLoading(false);
    }
  };

  useEffect(() => {
    fetchLeads();
  }, []);

  const updateStep = useCallback((toolName: string, status: "active" | "done") => {
    setSteps((prev) => prev.map((s) => s.id === toolName ? { ...s, status } : s));
  }, []);

  const handleRunAgent = useCallback((leadId: string) => {
    setIsLoading(true);
    setIsDone(false);
    setThoughts([]);
    setIsThinking(false);
    setCurrentLeadId(leadId);
    setSteps(INITIAL_STEPS);

    // Switch to generate tab to show progress
    setActiveTab("generate");

    const eventSource = new EventSource(`http://localhost:8000/api/agent/stream/${leadId}`);

    eventSource.addEventListener("tool_call", (e) => {
      const data = JSON.parse(e.data);
      updateStep(data.tool, "active");
    });
    eventSource.addEventListener("tool_result", (e) => {
      const data = JSON.parse(e.data);
      updateStep(data.tool, "done");
    });
    eventSource.addEventListener("thinking", (e) => {
      const data = JSON.parse(e.data);
      setIsThinking(true);
      setThoughts((prev) => [...prev, data.content]);
    });
    eventSource.addEventListener("done", () => {
      setIsDone(true);
      setIsLoading(false);
      setIsThinking(false);
      eventSource.close();
    });
    eventSource.onerror = () => {
      setIsLoading(false);
      setIsThinking(false);
      eventSource.close();
    };
  }, [updateStep]);

  const handleDeleteLead = async (leadId: string) => {
    if (!confirm(`Delete ${leadId}?`)) return;
    try {
      await fetch(`http://localhost:8000/api/leads/${leadId}`, { method: "DELETE" });
      fetchLeads();
    } catch (e) {
      console.error(e);
    }
  };

  const tabStyle = (tab: string) => ({
    padding: "10px 24px",
    background: activeTab === tab ? "#6366f1" : "transparent",
    color: activeTab === tab ? "#fff" : "#888",
    border: "none",
    borderRadius: 10,
    cursor: "pointer",
    fontWeight: 600,
    fontSize: 14,
    transition: "all 0.2s"
  });

  return (
    <div style={{ minHeight: "100vh", background: "#0a0a0f", color: "#e2e8f0" }}>
      {/* Header */}
      <div style={{
        borderBottom: "1px solid #2a2a4a",
        background: "#0d0d1f",
        padding: "16px 24px",
        display: "flex",
        alignItems: "center",
        gap: 12
      }}>
        <div style={{
          width: 36, height: 36, background: "#6366f1",
          borderRadius: 10, display: "flex", alignItems: "center",
          justifyContent: "center", fontSize: 18
        }}>🤖</div>
        <div>
          <div style={{ color: "#fff", fontWeight: 700, fontSize: 18, lineHeight: 1 }}>AgentIQ</div>
          <div style={{ color: "#666", fontSize: 12 }}>Agentic AI Sales Automation</div>
        </div>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 6 }}>
          <div style={{ width: 8, height: 8, background: "#4ade80", borderRadius: "50%" }} />
          <span style={{ color: "#4ade80", fontSize: 12 }}>Backend Online</span>
        </div>
      </div>

      {/* Tabs */}
      <div style={{
        borderBottom: "1px solid #2a2a4a",
        background: "#0d0d1f",
        padding: "0 24px",
        display: "flex",
        gap: 8
      }}>
        <button style={tabStyle("generate")} onClick={() => setActiveTab("generate")}>
          ⚡ Generate
        </button>
        <button style={tabStyle("leads")} onClick={() => { setActiveTab("leads"); fetchLeads(); }}>
          👥 Leads {leads.length > 0 && `(${leads.length})`}
        </button>
        <button style={tabStyle("batch")} onClick={() => setActiveTab("batch")}>
          📦 Batch
        </button>
      </div>

      {/* Content */}
      <div style={{ maxWidth: 760, margin: "0 auto", padding: "32px 24px" }}>

        {/* GENERATE TAB */}
        {activeTab === "generate" && (
          <>
            <LeadInput onSubmit={handleRunAgent} isLoading={isLoading} />
            {(isLoading || isDone) && (
              <>
                <StepTracker steps={steps} />
                <ReasoningStream thoughts={thoughts} isActive={isThinking} />
                <DownloadButton show={isDone} leadId={currentLeadId} />
              </>
            )}
            {!isLoading && !isDone && (
              <div style={{ textAlign: "center", paddingTop: 60 }}>
                <div style={{
                  width: 64, height: 64, background: "#1a1a3a",
                  borderRadius: 16, display: "flex", alignItems: "center",
                  justifyContent: "center", margin: "0 auto 16px", fontSize: 32
                }}>🤖</div>
                <h3 style={{ color: "#fff", fontSize: 20, fontWeight: 600, marginBottom: 8 }}>
                  Ready to Generate Proposals
                </h3>
                <p style={{ color: "#666", fontSize: 14, maxWidth: 380, margin: "0 auto 24px" }}>
                  Enter a Lead ID above or go to the Leads tab to manage and generate proposals.
                </p>
                <button
                  onClick={() => setActiveTab("leads")}
                  style={{
                    background: "transparent",
                    border: "1px solid #6366f1",
                    color: "#6366f1",
                    borderRadius: 10,
                    padding: "10px 24px",
                    cursor: "pointer",
                    fontWeight: 600
                  }}
                >
                  👥 View All Leads →
                </button>
              </div>
            )}
          </>
        )}

        {/* LEADS TAB */}
        {activeTab === "leads" && (
          <>
            <div style={{ marginBottom: 24 }}>
              <h2 style={{ color: "#fff", fontSize: 22, fontWeight: 700, marginBottom: 4 }}>
                Lead Management
              </h2>
              <p style={{ color: "#666", fontSize: 14 }}>
                Add leads manually and generate AI proposals for each one
              </p>
            </div>

            <LeadForm onLeadCreated={fetchLeads} />

            <div style={{
              background: "#111127",
              border: "1px solid #2a2a4a",
              borderRadius: 16,
              padding: 24
            }}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
                <h3 style={{ color: "#fff", fontSize: 16, fontWeight: 600 }}>
                  All Leads ({leads.length})
                </h3>
                <button
                  onClick={fetchLeads}
                  style={{
                    background: "transparent",
                    border: "1px solid #2a2a4a",
                    color: "#888",
                    borderRadius: 8,
                    padding: "6px 12px",
                    cursor: "pointer",
                    fontSize: 12
                  }}
                >
                  🔄 Refresh
                </button>
              </div>

              {leadsLoading ? (
                <p style={{ color: "#555", textAlign: "center", padding: 20 }}>Loading leads...</p>
              ) : (
                <LeadsList
                  leads={leads}
                  onRunAgent={handleRunAgent}
                  onDelete={handleDeleteLead}
                  isLoading={isLoading}
                  currentLeadId={currentLeadId}
                />
              )}
            </div>
          </>
        )}

        {/* BATCH TAB */}
        {activeTab === "batch" && (
          <>
            <div style={{ marginBottom: 24 }}>
              <h2 style={{ color: "#fff", fontSize: 22, fontWeight: 700, marginBottom: 4 }}>
                Batch Processing
              </h2>
              <p style={{ color: "#666", fontSize: 14 }}>
                Generate proposals for hundreds of leads simultaneously
              </p>
            </div>
            <BatchUpload />
          </>
        )}
      </div>
    </div>
  );
}