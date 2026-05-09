# from langchain.tools import tool
# from services.crm import fetch_lead
# from services.rag import search_knowledge_base
# from services.pdf import generate_pdf, save_pdf
# import asyncio


# # @tool
# # def crm_fetch_tool(lead_id: str) -> str:
# #     """
# #     Fetch lead and opportunity data from Salesforce CRM.
# #     Input: lead_id (string like LEAD_001)
# #     Output: Lead details including name, company, email, opportunities
# #     """
# #     data = fetch_lead(lead_id)
    
# #     # Format nicely for the agent
# #     result = f"""
# # CRM Data for {lead_id}:
# # - Name: {data.get('name')}
# # - Company: {data.get('company')}
# # - Email: {data.get('email')}
# # - Phone: {data.get('phone')}
# # - Status: {data.get('status')}
# # - Description: {data.get('description')}
# # - Opportunities: {data.get('opportunities')}
# #     """
# #     return result.strip()

# # global pdf_generated

# pdf_generated = False

# @tool
# def crm_fetch_tool(lead_id: str) -> str:
#     """
#     Fetch lead and opportunity data from Salesforce CRM.

#     Input:
#         lead_id (string like LEAD_001)

#     Output:
#         Formatted CRM data including name, company, email, and opportunities
#     """

#     data = fetch_lead(lead_id)

#     # Extract opportunities safely
#     opps = data.get("opportunities", [])

#     # Convert list → readable text
#     if opps:
#         opps_text = ""
#         for o in opps:
#             opps_text += (
#                 f"\n  - {o.get('Name')} | ₹{o.get('Amount')} | "
#                 f"{o.get('StageName')} | Close: {o.get('CloseDate')}"
#             )
#     else:
#         opps_text = " None"

#     result = f"""
# CRM Data for {lead_id}:
# - Name: {data.get('name')}
# - Company: {data.get('company')}
# - Email: {data.get('email')}
# - Phone: {data.get('phone')}
# - Status: {data.get('status')}
# - Description: {data.get('description')}
# - Opportunities:{opps_text}
#     """

#     return result.strip()


# @tool
# def rag_search_tool(query: str) -> str:
#     """
#     Search the knowledge base for relevant product and pricing information.
#     Input: search query string
#     Output: Relevant documents from knowledge base
#     """
#     return search_knowledge_base(query)


# @tool
# def pdf_generation_tool(proposal_text: str) -> str:
#     """
#     Generate a PDF proposal from the given proposal text.
#     Input: Complete proposal text in markdown format
#     Output: Confirmation that PDF was saved
#     """
#     global pdf_generated   # ✅ REQUIRED
#     # Extract lead name from proposal if possible
#     lead_name = "Client"
#     for line in proposal_text.split("\n"):
#         if "proposal for" in line.lower():
#             lead_name = line.split("for")[-1].strip()
#             break
    
#     if pdf_generated:
#         return "PDF already generated. Skipping duplicate call."

#     pdf_generated = True    
    
#     pdf_bytes = generate_pdf(proposal_text, lead_name)
    
#     # Save synchronously
#     path = f"tmp/proposal.pdf"
#     with open(path, "wb") as f:
#         f.write(pdf_bytes)
    
#     return f"PDF proposal generated and saved to {path}"


# TOOLS = [crm_fetch_tool, rag_search_tool, pdf_generation_tool]






# from langchain.tools import tool
# from services.crm import fetch_lead
# from services.rag import search_knowledge_base
# from services.pdf import generate_pdf
# import json

# @tool
# def crm_fetch_tool(lead_id: str) -> str:
#     """
#     Fetch lead and opportunity data from CRM.
#     Input: lead_id string
#     """
#     data = fetch_lead(lead_id)
#     return f"""
# Name: {data.get('name')}
# Company: {data.get('company')}
# Email: {data.get('email')}
# Phone: {data.get('phone')}
# Status: {data.get('status')}
# Description: {data.get('description')}
# Opportunities: {json.dumps(data.get('opportunities', []))}
# """.strip()


# @tool
# def rag_search_tool(query: str) -> str:
#     """
#     Search knowledge base for product and pricing information.
#     Input: search query string
#     """
#     return search_knowledge_base(query)


# @tool
# def pdf_generation_tool(proposal_text: str) -> str:
#     """
#     Generate PDF from proposal text.
#     Input: complete proposal text with real lead name and company
#     """
#     # Extract name from proposal for header
#     lead_name = "Client"
#     company = ""
    
#     for line in proposal_text.split("\n"):
#         line_lower = line.lower()
#         if "proposal" in line_lower and "—" in line:
#             parts = line.split("—")
#             if len(parts) > 1:
#                 name_part = parts[1].strip()
#                 if " at " in name_part:
#                     lead_name = name_part.split(" at ")[0].strip()
#                     company = name_part.split(" at ")[1].strip()
#                 else:
#                     lead_name = name_part
#             break
#         elif "dear " in line_lower:
#             name_part = line.lower().replace("dear ", "").replace(",", "").strip()
#             lead_name = name_part.title()
#             break

#     pdf_bytes = generate_pdf(proposal_text, f"{lead_name} at {company}".strip(" at"))
    
#     path = "tmp/proposal.pdf"
#     with open(path, "wb") as f:
#         f.write(pdf_bytes)
    
#     return f"PDF generated for {lead_name} at {company}, saved to {path}"


# TOOLS = [crm_fetch_tool, rag_search_tool, pdf_generation_tool]






from langchain.tools import tool
from services.crm import fetch_lead
from services.rag import search_knowledge_base
from services.pdf import generate_pdf
import json

# This gets set BEFORE agent runs each time
_current_lead = {}

def set_current_lead(lead_data: dict):
    global _current_lead
    _current_lead = lead_data

@tool
def crm_fetch_tool(lead_id: str) -> str:
    """Fetch lead data from CRM. Input: lead_id string"""
    # Always use the pre-set lead data, ignore what LLM passes
    data = _current_lead if _current_lead else fetch_lead(lead_id)
    return f"""
Name: {data.get('name')}
Company: {data.get('company')}
Email: {data.get('email')}
Description: {data.get('description')}
Opportunities: {json.dumps(data.get('opportunities', []))}
""".strip()

@tool
def rag_search_tool(query: str) -> str:
    """Search knowledge base. Input: search query"""
    return search_knowledge_base(query)

@tool
def pdf_generation_tool(proposal_text: str) -> str:
    """Generate PDF. Input: complete proposal text"""
    # Force use real lead data from global
    lead = _current_lead
    lead_name = lead.get("name", "Client")
    company = lead.get("company", "")
    
    # Force replace any wrong names in proposal
    wrong_names = ["Rahul Mehta", "TechCorp India", "LEAD_001", "LEAD_002", "LEAD_003"]
    fixed_text = proposal_text
    for wrong in wrong_names:
        if wrong != lead_name and wrong != company:
            fixed_text = fixed_text.replace(wrong, lead_name if "Mehta" in wrong or "Shah" in wrong or "Verma" in wrong else company)
    
    pdf_bytes = generate_pdf(fixed_text, f"{lead_name} at {company}")
    with open("tmp/proposal.pdf", "wb") as f:
        f.write(pdf_bytes)
    
    return f"PDF generated for {lead_name} at {company}"

TOOLS = [crm_fetch_tool, rag_search_tool, pdf_generation_tool]