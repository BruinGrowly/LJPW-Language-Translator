"""
LJPW REST API - Main Application
Runs on FastAPI.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path

# Handle import for both package and direct execution
try:
    from .core import get_engine
except ImportError:
    from core import get_engine

app = FastAPI(
    title="LJPW Semantic API",
    description="Universal Translation Semantic Space API",
    version="1.0.0"
)

# --- Models ---
class ConceptResponse(BaseModel):
    name: str
    definition: str
    coordinates: List[float]
    domain: str
    id: str

class AnalyzeRequest(BaseModel):
    text: str

class NeighborResponse(BaseModel):
    concept: ConceptResponse
    distance: float

# --- Static Files ---
# Mount static files (Frontend)
static_dir = Path(__file__).parent.parent / "web"
app.mount("/app", StaticFiles(directory=static_dir, html=True), name="static")

# --- Routes ---

@app.on_event("startup")
async def startup_event():
    get_engine() # Pre-load data

@app.get("/")
def read_root():
    return FileResponse(static_dir / "index.html")

@app.get("/api/root")
def read_api_root():
    engine = get_engine()
    return {
        "status": "online",
        "version": "1.0.0",
        "concepts_loaded": len(engine.concepts),
        "docs_url": "/docs"
    }

@app.get("/concepts/{name}", response_model=ConceptResponse)
def get_concept(name: str):
    engine = get_engine()
    concept = engine.get_concept(name)
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    return concept

@app.get("/neighbors/{name}")
def get_neighbors(name: str, n: int = 10):
    engine = get_engine()
    vector = engine.get_vector(name)
    if vector is None:
        raise HTTPException(status_code=404, detail="Concept not found")
        
    results = engine.search_nearest(vector.tolist(), n + 1) # +1 because it finds itself
    
    # Filter out self (distance 0)
    final = [r for r in results if r['id'] != name.lower()]
    return final[:n]

@app.post("/analyze/text")
def analyze_text_endpoint(req: AnalyzeRequest):
    engine = get_engine()
    result = engine.analyze_text(req.text)
    return result

@app.post("/vector")
def solve_vector(name: str):
    """Get vector for a name (helper for clients)."""
    engine = get_engine()
    vec = engine.get_vector(name)
    if vec is None:
         raise HTTPException(status_code=404, detail="Concept not found")
    return {"vector": vec.tolist()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
