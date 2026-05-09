# from fastapi import APIRouter, UploadFile, File
# import pandas as pd
# import asyncio
# import io
# from agent.graph import run_agent

# router = APIRouter(prefix="/api/batch")


# @router.post("/process-csv")
# async def process_csv(file: UploadFile = File(...)):
#     """Process hundreds of leads from CSV simultaneously"""
    
#     contents = await file.read()
#     df = pd.read_csv(io.BytesIO(contents))
    
#     if "lead_id" not in df.columns:
#         return {"error": "CSV must have a 'lead_id' column"}
    
#     lead_ids = df["lead_id"].tolist()
    
#     # Process all leads concurrently
#     tasks = [run_agent(lead_id) for lead_id in lead_ids]
#     results = await asyncio.gather(*tasks, return_exceptions=True)
    
#     output = []
#     for lead_id, result in zip(lead_ids, results):
#         if isinstance(result, Exception):
#             output.append({"lead_id": lead_id, "status": "failed", "error": str(result)})
#         else:
#             output.append({"lead_id": lead_id, "status": "success"})
    
#     return {
#         "total": len(lead_ids),
#         "processed": len([r for r in output if r["status"] == "success"]),
#         "failed": len([r for r in output if r["status"] == "failed"]),
#         "results": output
#     }






from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import asyncio
import io
from agent.graph import run_agent
from services.leads_db import get_all_leads

router = APIRouter(prefix="/api/batch")


@router.post("/process-csv")
async def process_csv(file: UploadFile = File(...)):
    """Process leads from uploaded CSV simultaneously"""
    contents = await file.read()

    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        return JSONResponse({"error": f"Invalid CSV: {str(e)}"}, status_code=400)

    if "lead_id" not in df.columns:
        return JSONResponse(
            {"error": "CSV must have a 'lead_id' column"},
            status_code=400
        )

    lead_ids = df["lead_id"].dropna().tolist()

    if not lead_ids:
        return JSONResponse({"error": "No lead IDs found"}, status_code=400)

    print(f"Batch processing {len(lead_ids)} leads: {lead_ids}")

    tasks = [run_agent(lead_id) for lead_id in lead_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    output = []
    for lead_id, result in zip(lead_ids, results):
        if isinstance(result, Exception):
            output.append({"lead_id": lead_id, "status": "failed", "error": str(result)})
        else:
            output.append({"lead_id": lead_id, "status": "success", "message": "Proposal generated"})

    return {
        "total": len(lead_ids),
        "success": len([r for r in output if r["status"] == "success"]),
        "failed": len([r for r in output if r["status"] == "failed"]),
        "results": output
    }


@router.post("/process-all")
async def process_all_leads():
    """Process ALL leads from Supabase at once"""
    leads = get_all_leads()
    lead_ids = [l["id"] for l in leads]

    if not lead_ids:
        return {"error": "No leads found in database"}

    print(f"Processing all {len(lead_ids)} leads")

    tasks = [run_agent(lead_id) for lead_id in lead_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    output = []
    for lead_id, result in zip(lead_ids, results):
        output.append({
            "lead_id": lead_id,
            "status": "failed" if isinstance(result, Exception) else "success"
        })

    return {
        "total": len(lead_ids),
        "success": len([r for r in output if r["status"] == "success"]),
        "results": output
    }