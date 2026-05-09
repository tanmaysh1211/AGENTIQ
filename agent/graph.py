# # from langgraph.prebuilt import create_react_agent
# # # from langchain.agents import create_react_agent
# # from langchain_groq import ChatGroq
# # from agent.tools import TOOLS
# # from agent.prompts import AGENT_SYSTEM_PROMPT
# # import os
# # from dotenv import load_dotenv

# # load_dotenv()

# # # Initialize LLM
# # llm = ChatGroq(
# #     model="llama-3.3-70b-versatile",
# #     api_key=os.getenv("GROQ_API_KEY"),
# #     temperature=0.3
# # )

# # # Create ReAct agent
# # agent_executor = create_react_agent(
# #     llm,
# #     TOOLS,
# #     # state_modifier=AGENT_SYSTEM_PROMPT
# # )


# # async def run_agent_stream(lead_id: str):
# #     """Stream agent reasoning steps"""
# #     inputs = {
# #         "messages": [{
# #             "role": "user",
# #             "content": f"Create a sales proposal for lead ID: {lead_id}"
# #         }]
# #     }
    
# #     async for event in agent_executor.astream_events(inputs, version="v1"):
# #         yield event


# # async def run_agent(lead_id: str) -> str:
# #     """Run agent and return final response"""
# #     inputs = {
# #         "messages": [{
# #             "role": "user",
# #             "content": f"Create a sales proposal for lead ID: {lead_id}"
# #         }]
# #     }
    
# #     result = await agent_executor.ainvoke(inputs)
# #     messages = result.get("messages", [])
    
# #     if messages:
# #         return messages[-1].content
# #     return "Agent completed but no response generated"










# from langgraph.prebuilt import create_react_agent
# from langchain_groq import ChatGroq
# from agent.tools import TOOLS
# from agent.prompts import AGENT_SYSTEM_PROMPT
# from services.crm import fetch_lead
# import os
# from dotenv import load_dotenv

# load_dotenv()

# llm = ChatGroq(
#     model="llama-3.3-70b-versatile",
#     api_key=os.getenv("GROQ_API_KEY"),
#     temperature=0.1
# )

# agent_executor = create_react_agent(
#     llm,
#     TOOLS,
#     prompt=AGENT_SYSTEM_PROMPT
# )


# # async def run_agent_stream(lead_id: str):
# #     """Stream agent reasoning steps"""
    
# #     # Pre-fetch CRM data and inject into prompt
# #     crm_data = fetch_lead(lead_id)
    
# #     inputs = {
# #         "messages": [{
# #             "role": "user",
# #             "content": f"""Create a detailed sales proposal for this lead:

# # Lead ID: {lead_id}
# # Name: {crm_data['name']}
# # Company: {crm_data['company']}
# # Email: {crm_data['email']}
# # Description: {crm_data['description']}
# # Opportunities: {crm_data['opportunities']}

# # Instructions:
# # 1. Call crm_fetch_tool with lead_id: {lead_id}
# # 2. Call rag_search_tool to search for relevant pricing and solutions
# # 3. Write a FULL detailed proposal using the REAL name "{crm_data['name']}" and company "{crm_data['company']}"
# # 4. Call pdf_generation_tool with the complete proposal text

# # IMPORTANT: The proposal must address {crm_data['name']} at {crm_data['company']} by name throughout.
# # Never use "{lead_id}" as a name in the proposal.
# # """
# #         }]
# #     }
    
# #     async for event in agent_executor.astream_events(inputs, version="v1"):
# #         yield event


# # async def run_agent(lead_id: str) -> str:
# #     """Run agent and return final response"""
# #     crm_data = fetch_lead(lead_id)
    
# #     inputs = {
# #         "messages": [{
# #             "role": "user",
# #             "content": f"""Create a sales proposal for:
# # Lead ID: {lead_id}
# # Name: {crm_data['name']}
# # Company: {crm_data['company']}
# # Description: {crm_data['description']}

# # Use tools in order: crm_fetch_tool → rag_search_tool → pdf_generation_tool
# # Address the proposal to {crm_data['name']} at {crm_data['company']}.
# # """
# #         }]
# #     }
    
# #     result = await agent_executor.ainvoke(inputs)
# #     messages = result.get("messages", [])
# #     if messages:
# #         return messages[-1].content
# #     return "Agent completed"



# async def run_agent_stream(lead_id: str):
#     """Stream agent reasoning steps"""
    
#     # Pre-fetch CRM data and inject into prompt
#     crm_data = fetch_lead(lead_id)
    
#     # Safely get opportunity details
#     opp = crm_data['opportunities'][0] if crm_data['opportunities'] else {}
#     deal_amount = opp.get('Amount', 'TBD')
#     deal_stage = opp.get('StageName', 'New')
#     deal_name = opp.get('Name', 'General Inquiry')
    
#     inputs = {
#         "messages": [{
#             "role": "user",
#             "content": f"""Create a detailed sales proposal for this specific lead:

# Lead ID: {lead_id}
# Name: {crm_data['name']}
# Company: {crm_data['company']}
# Email: {crm_data['email']}
# Description: {crm_data['description']}
# Current Deal: {deal_name}
# Deal Value: ${deal_amount}
# Deal Stage: {deal_stage}

# Follow these steps EXACTLY:
# 1. Call crm_fetch_tool with lead_id="{lead_id}"
# 2. Call rag_search_tool with a query matching their needs: "{crm_data['description']}"
# 3. Write a COMPLETE personalized proposal for {crm_data['name']} at {crm_data['company']}
#    - Mention their company "{crm_data['company']}" specifically
#    - Recommend a plan that fits their budget of ${deal_amount}
#    - Reference their specific need: "{crm_data['description']}"
# 4. Call pdf_generation_tool with the full proposal

# CRITICAL: 
# - Use "{crm_data['name']}" as the person's name throughout
# - Use "{crm_data['company']}" as their company throughout  
# - NEVER write "LEAD_001" or any lead ID as a name
# - Tailor pricing recommendation to their ${deal_amount} budget
# """
#         }]
#     }
    
#     async for event in agent_executor.astream_events(inputs, version="v1"):
#         yield event


# async def run_agent(lead_id: str) -> str:
#     """Run agent and return final response"""
#     crm_data = fetch_lead(lead_id)
#     opp = crm_data['opportunities'][0] if crm_data['opportunities'] else {}
#     deal_amount = opp.get('Amount', 'TBD')
    
#     inputs = {
#         "messages": [{
#             "role": "user",
#             "content": f"""Create a sales proposal for:
# Name: {crm_data['name']}
# Company: {crm_data['company']}
# Description: {crm_data['description']}
# Budget: ${deal_amount}

# Use tools: crm_fetch_tool({lead_id}) → rag_search_tool → pdf_generation_tool
# Address proposal to {crm_data['name']} at {crm_data['company']}.
# """
#         }]
#     }
    
#     result = await agent_executor.ainvoke(inputs)
#     messages = result.get("messages", [])
#     if messages:
#         return messages[-1].content
#     return "Agent completed"










from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from agent.tools import TOOLS, set_current_lead
from agent.prompts import AGENT_SYSTEM_PROMPT
from services.crm import fetch_lead
import os
from dotenv import load_dotenv

load_dotenv()

def get_agent():
    return create_react_agent(
        ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.1
        ),
        TOOLS,
        prompt=AGENT_SYSTEM_PROMPT
    )

async def run_agent_stream(lead_id: str):
    crm_data = fetch_lead(lead_id)
    
    # SET GLOBAL LEAD DATA BEFORE AGENT RUNS
    set_current_lead(crm_data)
    
    opp = crm_data['opportunities'][0] if crm_data['opportunities'] else {}
    deal_amount = opp.get('Amount', 'TBD')

    agent = get_agent()

    inputs = {
        "messages": [{
            "role": "user",
            "content": f"""Create a sales proposal.

Use these tools in order:
1. crm_fetch_tool("{lead_id}")
2. rag_search_tool("{crm_data['description']}")
3. pdf_generation_tool(complete proposal text)

The lead is {crm_data['name']} at {crm_data['company']} with budget ${deal_amount}.
"""
        }]
    }

    async for event in agent.astream_events(inputs, version="v1"):
        yield event

async def run_agent(lead_id: str) -> str:
    crm_data = fetch_lead(lead_id)
    set_current_lead(crm_data)
    
    agent = get_agent()
    inputs = {
        "messages": [{
            "role": "user", 
            "content": f"Create proposal for {crm_data['name']} at {crm_data['company']}. Use crm_fetch_tool({lead_id}), rag_search_tool, then pdf_generation_tool."
        }]
    }
    result = await agent.ainvoke(inputs)
    messages = result.get("messages", [])
    return messages[-1].content if messages else "Done"