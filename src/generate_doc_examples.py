import os
import sys
import json
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

SEEDS = [
    "Floor length chiffon bridesmaid dress with pleated bodice and V neckline available in sage and dusty blue",
    "Sparkly sequin fitted prom gown featuring a deep illusion neckline and open back",
    "Off shoulder satin ball gown with corset bodice and sweep train in royal navy",
    "Lace mermaid wedding dress with long sleeves and scalloped hem",
    "Short cocktail dress with feather trim and beaded waist detail",
    "Tulle A line evening gown with floral embroidery and cap sleeves",
    "Stretch jersey sheath dress with ruched waist and side slit",
    "Strapless sweetheart neckline glitter gown with layered skirt",
    "One shoulder draped chiffon dress with high slit and empire waist",
    "Velvet winter formal dress with square neckline and puff sleeves"
]

def main():
    out = []
    out.append("## Verbatim Extraction Examples\n")
    out.append("Below are the exact request and response pairs for the 10 seed sentences run through the `POST /extract` API using the default `ml` strategy:\n")
    
    for idx, text in enumerate(SEEDS):
        payload = {"description": text}
        response = client.post("/extract", json=payload)
        res_data = response.json()
        
        out.append(f"### Example {idx+1}\n")
        out.append(f"**Request Description:**\n> \"{text}\"\n")
        out.append("```bash")
        out.append(f"curl -X 'POST' \\")
        out.append(f"  'http://localhost:8000/extract' \\")
        out.append(f"  -H 'Content-Type: application/json' \\")
        out.append(f"  -d '{json.dumps(payload)}'")
        out.append("```\n")
        out.append("**API Response:**")
        out.append("```json")
        out.append(json.dumps(res_data, indent=2))
        out.append("```\n")
        out.append("---")
        out.append("")
        
    output_path = "doc_examples.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"Successfully wrote examples to {output_path}")

if __name__ == "__main__":
    main()
