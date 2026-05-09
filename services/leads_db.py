from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def generate_lead_id() -> str:
    """Auto generate next lead ID"""
    result = supabase.table("leads").select("id").execute()
    existing = [r["id"] for r in result.data]
    
    # Find next number
    nums = []
    for lid in existing:
        try:
            nums.append(int(lid.replace("LEAD_", "")))
        except:
            pass
    
    next_num = max(nums) + 1 if nums else 1
    return f"LEAD_{str(next_num).zfill(3)}"


def create_lead(data: dict) -> dict:
    """Create new lead in Supabase"""
    lead_id = generate_lead_id()
    
    lead = {
        "id": lead_id,
        "name": data.get("name"),
        "company": data.get("company"),
        "email": data.get("email", ""),
        "phone": data.get("phone", ""),
        "status": data.get("status", "New"),
        "description": data.get("description", ""),
        "deal_name": data.get("deal_name", "General Inquiry"),
        "deal_amount": data.get("deal_amount", 0),
        "deal_stage": data.get("deal_stage", "Prospecting"),
        "created_at": datetime.now().isoformat()
    }
    
    result = supabase.table("leads").insert(lead).execute()
    return result.data[0] if result.data else lead


def get_all_leads() -> list:
    """Get all leads from Supabase"""
    result = supabase.table("leads").select("*").order("created_at", desc=True).execute()
    return result.data


def get_lead(lead_id: str) -> dict:
    """Get single lead by ID"""
    result = supabase.table("leads").select("*").eq("id", lead_id).execute()
    if result.data:
        return result.data[0]
    return {}


def delete_lead(lead_id: str) -> bool:
    """Delete lead by ID"""
    result = supabase.table("leads").delete().eq("id", lead_id).execute()
    return True


def update_lead(lead_id: str, data: dict) -> dict:
    """Update existing lead"""
    result = supabase.table("leads").update(data).eq("id", lead_id).execute()
    return result.data[0] if result.data else {}