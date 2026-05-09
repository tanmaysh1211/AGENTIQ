from sentence_transformers import SentenceTransformer
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

# Load embedding model once at startup
model = SentenceTransformer("all-MiniLM-L6-v2")

# Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


def ingest_document(text: str) -> dict:
    """Embed and store a document in Supabase"""
    try:
        embedding = model.encode(text).tolist()
        
        result = supabase.table("documents").insert({
            "content": text,
            "embedding": embedding
        }).execute()
        
        return {"status": "success", "data": result.data}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}


def search_knowledge_base(query: str, match_count: int = 5) -> str:
    """Search vector DB for relevant documents"""
    try:
        query_embedding = model.encode(query).tolist()
        
        result = supabase.rpc("match_documents", {
            "query_embedding": query_embedding,
            "match_count": match_count
        }).execute()
        
        if not result.data:
            return "No relevant documents found in knowledge base."
        
        # Format results
        docs = []
        for i, doc in enumerate(result.data):
            similarity = round(doc.get("similarity", 0) * 100, 1)
            docs.append(f"[Doc {i+1} - {similarity}% match]\n{doc['content']}")
        
        return "\n\n---\n\n".join(docs)
    
    except Exception as e:
        return f"RAG search error: {str(e)}"


def ingest_sample_knowledge():
    """Seed the knowledge base with sample product data"""
    sample_docs = [
        """AgentIQ Pro Plan: $499/month
        Features: Unlimited AI proposals, CRM sync, PDF export,
        Priority support, Custom branding, API access.
        Best for: Mid-size companies with 50+ leads/month.""",
        
        """AgentIQ Starter Plan: $99/month
        Features: 50 AI proposals/month, Basic CRM integration,
        PDF export, Email support.
        Best for: Small businesses and startups.""",
        
        """AgentIQ Enterprise Plan: Custom pricing
        Features: Unlimited everything, Dedicated account manager,
        Custom AI training, SLA guarantee, On-premise option.
        Best for: Large enterprises with complex sales cycles.""",
        
        """AgentIQ ROI Statistics:
        - Average 60% reduction in proposal drafting time
        - 35% higher close rates with AI-personalized proposals
        - 100+ enterprise customers in 2025
        - Average setup time: 2 days""",
        
        """AgentIQ Integration Support:
        Supports Salesforce, HubSpot, Pipedrive CRM systems.
        REST API available. Webhook support for real-time sync.
        SSO with Google and Microsoft."""
    ]
    
    print("Seeding knowledge base...")
    for doc in sample_docs:
        result = ingest_document(doc)
        print(f"Ingested: {result['status']}")
    print("Knowledge base ready!")