from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.leads_db import (
    create_lead, get_all_leads, 
    get_lead, delete_lead, update_lead
)

router = APIRouter(prefix="/api/leads")

class LeadCreate(BaseModel):
    name: str
    company: str
    email: str = ""
    phone: str = ""
    status: str = "New"
    description: str = ""
    deal_name: str = "General Inquiry"
    deal_amount: int = 0
    deal_stage: str = "Prospecting"

class LeadUpdate(BaseModel):
    name: str = None
    company: str = None
    email: str = None
    phone: str = None
    status: str = None
    description: str = None
    deal_name: str = None
    deal_amount: int = None
    deal_stage: str = None


@router.post("")
def create_new_lead(lead: LeadCreate):
    """Create a new lead"""
    data = lead.model_dump()
    result = create_lead(data)
    return {"success": True, "lead": result}


@router.get("")
def list_leads():
    """Get all leads"""
    leads = get_all_leads()
    return {"leads": leads, "total": len(leads)}


@router.get("/{lead_id}")
def get_single_lead(lead_id: str):
    """Get one lead by ID"""
    lead = get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.put("/{lead_id}")
def update_existing_lead(lead_id: str, lead: LeadUpdate):
    """Update a lead"""
    data = {k: v for k, v in lead.model_dump().items() if v is not None}
    result = update_lead(lead_id, data)
    return {"success": True, "lead": result}


@router.delete("/{lead_id}")
def delete_existing_lead(lead_id: str):
    """Delete a lead"""
    delete_lead(lead_id)
    return {"success": True, "message": f"{lead_id} deleted"}