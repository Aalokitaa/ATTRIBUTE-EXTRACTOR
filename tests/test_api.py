import os
import sys
# Add project root to path to resolve src and api imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "ml_model_loaded" in data

def test_extract_endpoint_rule_based():
    payload = {
        "description": "Floor length chiffon bridesmaid dress with pleated bodice and V neckline available in sage and dusty blue",
        "strategy": "rule_based"
    }
    response = client.post("/extract", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["Fabric"] == "chiffon"
    assert data["Neckline"] == "V neck"
    assert "sage" in data["Color"]
    assert "dusty blue" in data["Color"]
    assert data["Length"] == "floor length"
    assert data["Embellishment"] == "pleated"
    assert data["Category"] == "bridesmaid dress"
    assert data["strategy_used"] == "rule_based"
    assert data["matched_terms"] is not None

def test_extract_endpoint_ml():
    payload = {
        "description": "Floor length chiffon bridesmaid dress with pleated bodice and V neckline available in sage and dusty blue",
        "strategy": "ml"
    }
    response = client.post("/extract", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["Fabric"] == "chiffon"
    assert data["Neckline"] == "V neck"
    assert "sage" in data["Color"]
    assert "dusty blue" in data["Color"]
    assert data["strategy_used"] in ["ml", "rule_based"]
    assert "confidence" in data
