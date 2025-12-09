"""
Internal API Test
Uses TestClient to verify API without running a server.
"""

from fastapi.testclient import TestClient
from api.main import app
import json

client = TestClient(app)

def test_api():
    print("="*60)
    print("TESTING API ENDPOINTS")
    print("="*60)
    
    # 1. Health Check
    print("GET /")
    response = client.get("/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    
    # 2. Get Concept (Arts)
    print("\nGET /concepts/painting")
    response = client.get("/concepts/painting")
    if response.status_code == 200:
        data = response.json()
        print(f"Found: {data['name']} (Domain: {data['domain']})")
        print(f"Coords: {data['coordinates']}")
    else:
        print(f"Error: {response.text}")
        
    # 3. Get Neighbors (Affection)
    print("\nGET /neighbors/affection?n=5")
    response = client.get("/neighbors/affection?n=5")
    if response.status_code == 200:
        data = response.json()
        print(f"Neighbors for Affection:")
        for neighbor in data:
            print(f" - {neighbor['name']} (Dist: {neighbor['distance']:.4f})")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_api()
