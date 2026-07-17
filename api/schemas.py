from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class ExtractionRequest(BaseModel):
    description: str = Field(
        ..., 
        json_schema_extra={"example": "Floor length chiffon bridesmaid dress with pleated bodice and V neckline available in sage and dusty blue"},
        description="Unstructured fashion/apparel product description text to parse."
    )
    strategy: Optional[str] = Field(
        "ml", 
        json_schema_extra={"example": "ml"},
        description="Extraction strategy to use. Options are 'ml' (machine learning, default) or 'rule_based'."
    )

class AttributeConfidence(BaseModel):
    Silhouette: float = Field(..., description="Model confidence score for Silhouette prediction.")
    Fabric: float = Field(..., description="Model confidence score for Fabric prediction.")
    Neckline: float = Field(..., description="Model confidence score for Neckline prediction.")
    Sleeve: float = Field(..., description="Model confidence score for Sleeve prediction.")
    Length: float = Field(..., description="Model confidence score for Length prediction.")
    Embellishment: float = Field(..., description="Model confidence score for Embellishment prediction.")
    Color: float = Field(..., description="Model confidence score for Color prediction.")
    Category: float = Field(..., description="Model confidence score for Category prediction.")

class ExtractionResponse(BaseModel):
    Silhouette: Optional[str] = Field(None, description="Extracted canonical Silhouette name.")
    Fabric: Optional[str] = Field(None, description="Extracted canonical Fabric name.")
    Neckline: Optional[str] = Field(None, description="Extracted canonical Neckline name.")
    Sleeve: Optional[str] = Field(None, description="Extracted canonical Sleeve name.")
    Length: Optional[str] = Field(None, description="Extracted canonical Length name.")
    Embellishment: Optional[str] = Field(None, description="Extracted canonical Embellishment name.")
    Color: List[str] = Field(default_factory=list, description="List of extracted canonical Color names.")
    Category: Optional[str] = Field(None, description="Extracted canonical Category name.")
    strategy_used: str = Field(..., description="The extraction strategy that was used.")
    confidence: AttributeConfidence = Field(..., description="Confidence scores for all 8 attribute fields.")
    matched_terms: Optional[Dict[str, List[str]]] = Field(None, description="Specifically for rule_based strategy, lists the exact matched terms per field.")
