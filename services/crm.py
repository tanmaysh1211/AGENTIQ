# from simple_salesforce import Salesforce
# import os
# from dotenv import load_dotenv

# load_dotenv()

# def get_salesforce_client():
#     return Salesforce(
#         username=os.getenv("SF_USERNAME"),
#         password=os.getenv("SF_PASSWORD"),
#         security_token=os.getenv("SF_SECURITY_TOKEN")
#     )

# def fetch_lead(lead_id: str) -> dict:
#     try:
#         sf = get_salesforce_client()
        
#         # Fetch lead details
#         lead = sf.Lead.get(lead_id)
        
#         # Fetch related opportunities
#         opportunities = sf.query(
#             f"SELECT Name, Amount, StageName, CloseDate "
#             f"FROM Opportunity "
#             f"WHERE Lead__c = '{lead_id}'"
#         )
        
#         return {
#             "id": lead_id,
#             "name": lead.get("Name", ""),
#             "company": lead.get("Company", ""),
#             "email": lead.get("Email", ""),
#             "phone": lead.get("Phone", ""),
#             "status": lead.get("Status", ""),
#             "description": lead.get("Description", ""),
#             "opportunities": opportunities.get("records", [])
#         }
        
#     except Exception as e:
#         # Fallback mock data if Salesforce fails
#         print(f"Salesforce error: {e}, using mock data")
#         return get_mock_lead(lead_id)


# # def get_mock_lead(lead_id: str) -> dict:
# #     """Mock CRM data for testing"""
# #     mock_leads = {
# #         "LEAD_001": {
# #             "id": "LEAD_001",
# #             "name": "Rahul Mehta",
# #             "company": "TechCorp India",
# #             "email": "rahul@techcorp.com",
# #             "phone": "+91-9876543210",
# #             "status": "Working",
# #             "description": "Interested in enterprise AI solutions",
# #             "opportunities": [
# #                 {
# #                     "Name": "Enterprise AI Deal",
# #                     "Amount": 50000,
# #                     "StageName": "Negotiation",
# #                     "CloseDate": "2026-06-30"
# #                 }
# #             ]
# #         },
# #         "LEAD_002": {
# #             "id": "LEAD_002",
# #             "name": "Priya Shah",
# #             "company": "StartupXYZ",
# #             "email": "priya@startupxyz.com",
# #             "phone": "+91-9123456789",
# #             "status": "New",
# #             "description": "Looking for automation tools",
# #             "opportunities": [
# #                 {
# #                     "Name": "Starter Automation Plan",
# #                     "Amount": 5000,
# #                     "StageName": "Prospecting",
# #                     "CloseDate": "2026-05-15"
# #                 }
# #             ]
# #         },
# #         "LEAD_003": {
# #             "id": "LEAD_003",
# #             "name": "Amit Verma",
# #             "company": "FinanceHub",
# #             "email": "amit@financehub.com",
# #             "phone": "+91-9988776655",
# #             "status": "Working",
# #             "description": "Needs CRM + reporting integration",
# #             "opportunities": [
# #                 {
# #                     "Name": "CRM Integration Package",
# #                     "Amount": 25000,
# #                     "StageName": "Proposal",
# #                     "CloseDate": "2026-07-01"
# #                 }
# #             ]
# #         }
# #     }
    
# #     return mock_leads.get(lead_id, {
# #         "id": lead_id,
# #         "name": "Unknown Lead",
# #         "company": "Unknown",
# #         "email": "",
# #         "phone": "",
# #         "status": "New",
# #         "description": "",
# #         "opportunities": []
# #     })







# def get_mock_lead(lead_id: str) -> dict:
#     mock_leads = {
#         "LEAD_001": {
#             "id": "LEAD_001",
#             "name": "Rahul Mehta",
#             "company": "TechCorp India",
#             "email": "rahul@techcorp.com",
#             "phone": "+91-9876543210",
#             "status": "Working",
#             "description": "Interested in enterprise AI solutions for large scale automation",
#             "opportunities": [{"Name": "Enterprise AI Deal", "Amount": 50000, "StageName": "Negotiation"}]
#         },
#         "LEAD_002": {
#             "id": "LEAD_002",
#             "name": "Priya Shah",
#             "company": "StartupXYZ",
#             "email": "priya@startupxyz.com",
#             "phone": "+91-9123456789",
#             "status": "New",
#             "description": "Early stage startup looking for affordable automation tools to scale quickly",
#             "opportunities": [{"Name": "Starter Automation Plan", "Amount": 5000, "StageName": "Prospecting"}]
#         },
#         "LEAD_003": {
#             "id": "LEAD_003",
#             "name": "Amit Verma",
#             "company": "FinanceHub",
#             "email": "amit@financehub.com",
#             "phone": "+91-9988776655",
#             "status": "Working",
#             "description": "Finance company needing CRM integration and automated reporting pipelines",
#             "opportunities": [{"Name": "CRM Integration Package", "Amount": 25000, "StageName": "Proposal"}]
#         }
#     }
#     return mock_leads.get(lead_id, {
#         "id": lead_id, "name": "Unknown", "company": "Unknown",
#         "email": "", "phone": "", "status": "New",
#         "description": "", "opportunities": []
#     })









from dotenv import load_dotenv
import os

load_dotenv()

def fetch_lead(lead_id: str) -> dict:
    """Fetch lead - tries Supabase first, then mock fallback"""
    try:
        from services.leads_db import get_lead as get_lead_from_db
        data = get_lead_from_db(lead_id)
        if data:
            return {
                "id": data["id"],
                "name": data["name"],
                "company": data["company"],
                "email": data.get("email", ""),
                "phone": data.get("phone", ""),
                "status": data.get("status", "New"),
                "description": data.get("description", ""),
                "opportunities": [{
                    "Name": data.get("deal_name", "General"),
                    "Amount": data.get("deal_amount", 0),
                    "StageName": data.get("deal_stage", "New")
                }]
            }
    except Exception as e:
        print(f"Supabase lead fetch error: {e}")

    return get_mock_lead(lead_id)


def get_mock_lead(lead_id: str) -> dict:
    """Fallback mock data"""
    mock_leads = {
        "LEAD_001": {
            "id": "LEAD_001",
            "name": "Rahul Mehta",
            "company": "TechCorp India",
            "email": "rahul@techcorp.com",
            "phone": "+91-9876543210",
            "status": "Working",
            "description": "Interested in enterprise AI solutions for large scale automation",
            "opportunities": [{"Name": "Enterprise AI Deal", "Amount": 50000, "StageName": "Negotiation"}]
        },
        "LEAD_002": {
            "id": "LEAD_002",
            "name": "Priya Shah",
            "company": "StartupXYZ",
            "email": "priya@startupxyz.com",
            "phone": "+91-9123456789",
            "status": "New",
            "description": "Early stage startup looking for affordable automation tools to scale quickly",
            "opportunities": [{"Name": "Starter Automation Plan", "Amount": 5000, "StageName": "Prospecting"}]
        },
        "LEAD_003": {
            "id": "LEAD_003",
            "name": "Amit Verma",
            "company": "FinanceHub",
            "email": "amit@financehub.com",
            "phone": "+91-9988776655",
            "status": "Working",
            "description": "Finance company needing CRM integration and automated reporting pipelines",
            "opportunities": [{"Name": "CRM Integration Package", "Amount": 25000, "StageName": "Proposal"}]
        }
    }
    return mock_leads.get(lead_id, {
        "id": lead_id, "name": "Unknown", "company": "Unknown",
        "email": "", "phone": "", "status": "New",
        "description": "", "opportunities": []
    })