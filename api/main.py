import os
import sys
# Add project root to path to resolve src and api imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import ExtractionRequest, ExtractionResponse, AttributeConfidence
from src.models.rule_based_extractor import RuleBasedExtractor
from src.models.ml_extractor import MLExtractor

app = FastAPI(
    title="Product Attribute Extraction API",
    description="FastAPI service to extract structured fashion/apparel attributes from descriptions.",
    version="1.0.0"
)

# Enable CORS for frontend integration (e.g. standalone file usage)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate extractors
rule_extractor = RuleBasedExtractor()
ml_extractor = MLExtractor()

@app.get("/", response_class=HTMLResponse)
def read_frontend():
    """
    Serves the single-page frontend.
    """
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html"))
    if os.path.exists(frontend_path):
        with open(frontend_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h3>Frontend index.html not found</h3>", status_code=404)

@app.get("/health")
def health_check():
    """
    Returns service health status and indicating whether the ML model is loaded.
    """
    # Proactively check if model can be reloaded/loaded if it wasn't initially
    if not ml_extractor.loaded:
        ml_extractor.load_model()
        
    return {
        "status": "healthy",
        "ml_model_loaded": ml_extractor.loaded
    }

@app.post("/extract", response_model=ExtractionResponse)
def extract_attributes(request: ExtractionRequest):
    """
    Extract structured apparel attributes from a product description.
    Supports 'ml' and 'rule_based' extraction strategies.
    """
    description = request.description.strip()
    if not description:
        raise HTTPException(status_code=400, detail="Description text cannot be empty.")

    strategy = request.strategy.lower() if request.strategy else "ml"
    
    # Reload model if needed
    if strategy == "ml" and not ml_extractor.loaded:
        ml_extractor.load_model()

    if strategy == "ml":
        if ml_extractor.loaded:
            result = ml_extractor.extract(description)
            strategy_used = "ml"
        else:
            # Fallback to rule-based strategy if model artifact is missing
            result = rule_extractor.extract(description)
            strategy_used = "rule_based"
            print("Warning: ML model not loaded. Fell back to rule_based extraction.")
    elif strategy == "rule_based":
        result = rule_extractor.extract(description)
        strategy_used = "rule_based"
    else:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid strategy '{strategy}'. Allowed values are 'ml' or 'rule_based'."
        )

    # Format response
    confidence_data = AttributeConfidence(
        Silhouette=result["confidence"].get("Silhouette", 0.0),
        Fabric=result["confidence"].get("Fabric", 0.0),
        Neckline=result["confidence"].get("Neckline", 0.0),
        Sleeve=result["confidence"].get("Sleeve", 0.0),
        Length=result["confidence"].get("Length", 0.0),
        Embellishment=result["confidence"].get("Embellishment", 0.0),
        Color=result["confidence"].get("Color", 0.0),
        Category=result["confidence"].get("Category", 0.0)
    )

    return ExtractionResponse(
        Silhouette=result.get("Silhouette"),
        Fabric=result.get("Fabric"),
        Neckline=result.get("Neckline"),
        Sleeve=result.get("Sleeve"),
        Length=result.get("Length"),
        Embellishment=result.get("Embellishment"),
        Color=result.get("Color", []),
        Category=result.get("Category"),
        strategy_used=strategy_used,
        confidence=confidence_data,
        matched_terms=result.get("matched_terms")
    )
