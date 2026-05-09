# from fastapi import APIRouter
# from fastapi.responses import StreamingResponse, FileResponse
# from sse_starlette.sse import EventSourceResponse
# from agent.graph import run_agent_stream
# import json

# router = APIRouter(prefix="/api/agent")

# @router.get("/stream/{lead_id}")
# async def stream_agent(lead_id: str):
#     """Stream live reasoning steps to frontend via SSE"""
    
#     async def event_generator():
#         async for event in run_agent_stream(lead_id):
#             event_type = event.get("event")
            
#             if event_type == "on_chat_model_stream":
#                 # LLM thinking
#                 chunk = event["data"]["chunk"].content
#                 yield {
#                     "event": "thinking",
#                     "data": json.dumps({"step": "reasoning", "content": chunk})
#                 }
            
#             elif event_type == "on_tool_start":
#                 # Tool being called
#                 tool_name = event["name"]
#                 yield {
#                     "event": "tool_call",
#                     "data": json.dumps({"step": tool_name, "status": "started"})
#                 }
            
#             elif event_type == "on_tool_end":
#                 tool_name = event["name"]
#                 yield {
#                     "event": "tool_result",
#                     "data": json.dumps({"step": tool_name, "status": "done"})
#                 }
    
#     return EventSourceResponse(event_generator())


# @router.post("/export-pdf")
# async def export_pdf():
#     """Return the generated PDF file"""
#     return FileResponse(
#         "/tmp/proposal.pdf",
#         media_type="application/pdf",
#         filename="proposal.pdf"
#     )






from fastapi import APIRouter
from fastapi.responses import FileResponse
from sse_starlette.sse import EventSourceResponse
from agent.graph import run_agent_stream
import json

router = APIRouter(prefix="/api/agent")


@router.get("/stream/{lead_id}")
async def stream_agent(lead_id: str):
    """Stream live agent reasoning via SSE"""

    final_sent = False
    thinking_buffer = ""

    async def event_generator():
        nonlocal final_sent, thinking_buffer

        try:
            async for event in run_agent_stream(lead_id):

                events = []
                if isinstance(event, list):
                    events.extend(event)
                elif isinstance(event, dict):
                    events.append(event)
                else:
                    continue

                for e in events:
                    if not isinstance(e, dict):
                        continue

                    event_type = e.get("event", "")
                    data = e.get("data") if isinstance(e.get("data"), dict) else {}

                    # =========================
                    # 🧠 LLM STREAM
                    # =========================
                    if event_type == "on_chat_model_stream":
                        chunk = data.get("chunk")

                        if chunk and hasattr(chunk, "content") and chunk.content:
                            thinking_buffer += chunk.content

                            if len(thinking_buffer) > 40:
                                yield {
                                    "event": "thinking",
                                    "data": json.dumps({
                                        "step": "Agent Reasoning",
                                        "content": thinking_buffer
                                    })
                                }
                                thinking_buffer = ""

                    # =========================
                    # 🔧 TOOL START
                    # =========================
                    elif event_type == "on_tool_start":
                        yield {
                            "event": "tool_call",
                            "data": json.dumps({
                                "step": get_step_label(e.get("name", "unknown")),
                                "tool": e.get("name", "unknown"),
                                "input": str(data.get("input", {})),
                                "status": "started"
                            })
                        }

                    # =========================
                    # ✅ TOOL END
                    # =========================
                    elif event_type == "on_tool_end":
                        yield {
                            "event": "tool_result",
                            "data": json.dumps({
                                "step": get_step_label(e.get("name", "unknown")),
                                "tool": e.get("name", "unknown"),
                                "status": "completed"
                            })
                        }

                    # =========================
                    # 🏁 FINAL OUTPUT
                    # =========================
                    elif event_type == "on_chain_end" and not final_sent:
                        output = data.get("output", {})
                        messages = output.get("messages", []) if isinstance(output, dict) else []

                        final = ""   # ✅ ALWAYS define first

                        if messages:
                            last = messages[-1]
                            final = last.content if hasattr(last, "content") else ""

                            if final:
                                yield {
                                    "event": "done",
                                    "data": json.dumps({
                                        "step": "Complete",
                                        "content": final,
                                        "status": "done"
                                    })
                                }
                                final_sent = True
                                break

            # ✅ 🔥 THIS IS THE CORRECT PLACE (END FLUSH)
            if thinking_buffer:
                yield {
                    "event": "thinking",
                    "data": json.dumps({
                    "step": "Agent Reasoning",
                    "content": thinking_buffer
                    })
                }

        except Exception as e:
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }
    return EventSourceResponse(event_generator())

    # async def event_generator():
    #     try:
    #         async for event in run_agent_stream(lead_id):
    #             # print("EVENT TYPE:", type(event), event)

    #             # 🔥 Normalize event → always work with dicts
    #             events = []

    #             if isinstance(event, list):
    #                 events.extend(event)
    #             elif isinstance(event, dict):
    #                 events.append(event)
    #             else:
    #                 continue  # ignore garbage

    #             for e in events:
    #                 if not isinstance(e, dict):
    #                     continue

    #                 event_type = e.get("event", "")

    #                 # Safe data extraction
    #                 data = e.get("data") if isinstance(e.get("data"), dict) else {}

    #                 # =========================
    #                 # 🧠 LLM STREAM
    #                 # =========================
    #                 if event_type == "on_chat_model_stream":
    #                     chunk = data.get("chunk")

    #                     if chunk and hasattr(chunk, "content") and chunk.content:
    #                         thinking_buffer += chunk.content

    #     # send only when meaningful chunk formed
    #                     if len(thinking_buffer) > 40:
    #                         yield {
    #                             "event": "thinking",
    #                             "data": json.dumps({
    #                                 "step": "Agent Reasoning",
    #                                 "content": thinking_buffer
    #                             })
    #                         }
    #                         thinking_buffer = ""

    #                 # =========================
    #                 # 🔧 TOOL START
    #                 # =========================
    #                 elif event_type == "on_tool_start":
    #                     tool_name = e.get("name", "unknown")
    #                     tool_input = data.get("input", {})

    #                     yield {
    #                         "event": "tool_call",
    #                         "data": json.dumps({
    #                             "step": get_step_label(tool_name),
    #                             "tool": tool_name,
    #                             "input": str(tool_input),
    #                             "status": "started"
    #                         })
    #                     }

    #                 # =========================
    #                 # ✅ TOOL END
    #                 # =========================
    #                 elif event_type == "on_tool_end":
    #                     tool_name = e.get("name", "unknown")

    #                     yield {
    #                         "event": "tool_result",
    #                         "data": json.dumps({
    #                             "step": get_step_label(tool_name),
    #                             "tool": tool_name,
    #                             "status": "completed"
    #                         })
    #                     }

    #                 # =========================
    #                 # 🏁 FINAL OUTPUT
    #                 # =========================
    #                 # elif event_type == "on_chain_end":
    #                 #     output = data.get("output", {}) if isinstance(data.get("output"), dict) else {}
    #                 #     messages = output.get("messages", []) if isinstance(output, dict) else []

    #                 #     if messages:
    #                 #         last = messages[-1]
    #                 #         final = last.content if hasattr(last, "content") else ""

    #                 #         if final:
    #                 #             yield {
    #                 #                 "event": "done",
    #                 #                 "data": json.dumps({
    #                 #                     "step": "Complete",
    #                 #                     "content": final,
    #                 #                     "status": "done"
    #                 #                 })
    #                 #             }
    #                 elif event_type == "on_chain_end" and not final_sent:
    #                     output = data.get("output", {}) if isinstance(data.get("output"), dict) else {}
    #                     messages = output.get("messages", []) if isinstance(output, dict) else []

    #                     if messages:
    #                         last = messages[-1]
    #                         final = last.content if hasattr(last, "content") else ""

    #                     if final:
    #                         yield {
    #                             "event": "done",
    #                             "data": json.dumps({
    #                                 "step": "Complete",
    #                                 "content": final,
    #                                 "status": "done"
    #                             })
    #                         }
    #                         final_sent = True

    #     except Exception as e:
    #         yield {
    #             "event": "error",
    #             "data": json.dumps({"error": str(e)})
    #         }
    
    # async def event_generator():
    #     try:
    #         async for event in run_agent_stream(lead_id):
    #             print("EVENT TYPE:", type(event), event)

    #             if not isinstance(event, dict):
    #                 continue

    #             event_type = event.get("event", "")
    #             # event_type = event.get("event", "")
                
    #             # LLM is thinking/generating
    #             if event_type == "on_chat_model_stream":
    #                 # chunk = event.get("data", {}).get("chunk")
    #                 data = event.get("data") if isinstance(event.get("data"), dict) else {}
    #                 chunk = data.get("chunk")
    #                 if chunk and hasattr(chunk, "content") and chunk.content:
    #                     yield {
    #                         "event": "thinking",
    #                         "data": json.dumps({
    #                             "step": "Agent Reasoning",
    #                             "content": chunk.content
    #                         })
    #                     }
                
    #             # Tool is being called
    #             elif event_type == "on_tool_start":
    #                 tool_name = event.get("name", "unknown")
    #                 tool_input = event.get("data", {}).get("input", {})
    #                 yield {
    #                     "event": "tool_call",
    #                     "data": json.dumps({
    #                         "step": get_step_label(tool_name),
    #                         "tool": tool_name,
    #                         "input": str(tool_input),
    #                         "status": "started"
    #                     })
    #                 }
                
    #             # Tool finished
    #             elif event_type == "on_tool_end":
    #                 tool_name = event.get("name", "unknown")
    #                 yield {
    #                     "event": "tool_result",
    #                     "data": json.dumps({
    #                         "step": get_step_label(tool_name),
    #                         "tool": tool_name,
    #                         "status": "completed"
    #                     })
    #                 }
                
    #             # Agent finished
    #             elif event_type == "on_chain_end":
    #                 output = event.get("data", {}).get("output", {})
    #                 messages = output.get("messages", [])
    #                 if messages:
    #                     final = messages[-1].content if hasattr(messages[-1], "content") else ""
    #                     if final:
    #                         yield {
    #                             "event": "done",
    #                             "data": json.dumps({
    #                                 "step": "Complete",
    #                                 "content": final,
    #                                 "status": "done"
    #                             })
    #                         }
        
    #     except Exception as e:
    #         yield {
    #             "event": "error",
    #             "data": json.dumps({"error": str(e)})
    #         }
    
    # return EventSourceResponse(event_generator())


@router.post("/export-pdf")
async def export_pdf():
    """Download the generated PDF"""
    pdf_path = "tmp/proposal.pdf"
    
    import os
    if not os.path.exists(pdf_path):
        return {"error": "No PDF found. Run the agent first."}
    
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="agentiq_proposal.pdf"
    )


def get_step_label(tool_name: str) -> str:
    labels = {
        "crm_fetch_tool": "Fetching CRM Data",
        "rag_search_tool": "Searching Knowledge Base",
        "pdf_generation_tool": "Generating PDF Proposal"
    }
    return labels.get(tool_name, tool_name)