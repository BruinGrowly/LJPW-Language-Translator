"""
Internal Analysis Test
Verifies "Love" patch and Analysis endpoint.
"""

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_features():
    print("="*60)
    print("TESTING REFINEMENTS")
    print("="*60)
    
    # 1. Check Love Patch
    print("GET /concepts/love")
    res = client.get("/concepts/love")
    if res.status_code == 200:
        print("SUCCESS: Found 'Love'!")
        print(res.json()['coordinates'])
    else:
        print(f"FAIL: Love not found. {res.status_code}")

    # 2. Analyze Text
    print("\nPOST /analyze/text")
    payload = {"text": "Justice without power is empty."}
    res = client.post("/analyze/text", json=payload)
    if res.status_code == 200:
        data = res.json()
        print("SUCCESS: Analysis Result:")
        print(f"Coordinates: {data['coordinates']}")
        print(f"Dominant: {data['dominant']}")
        print(f"Words: {data['words_found']}")
    else:
        print(f"FAIL: Analysis error. {res.text}")

if __name__ == "__main__":
    test_features()
