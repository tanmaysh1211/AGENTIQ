from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.agent import router as agent_router
from routes.batch import router as batch_router
from routes.leads import router as leads_router
from services.rag import ingest_sample_knowledge
import os

app = FastAPI(
    title="AgentIQ",
    description="Agentic AI Sales Automation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router)
app.include_router(batch_router)
app.include_router(leads_router)


@app.on_event("startup")
async def startup():
    """Seed knowledge base on startup"""
    print("Starting AgentIQ...")
    os.makedirs("tmp", exist_ok=True)
    ingest_sample_knowledge()
    print("AgentIQ ready!")


@app.get("/")
def root():
    return {"message": "AgentIQ is running!"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "AgentIQ"}