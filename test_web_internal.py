"""
Internal Web Test
Verifies that static files are served correctly.
"""

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_web():
    print("="*60)
    print("TESTING WEB INTERFACE")
    print("="*60)
    
    # 1. Index
    print("GET /")
    response = client.get("/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200 and "<!DOCTYPE html>" in response.text:
        print("SUCCESS: HTML served.")
    else:
        print(f"FAIL: {response.text[:100]}")
        
    # 2. Style
    print("\nGET /app/style.css")
    response = client.get("/app/style.css")
    print(f"Status: {response.status_code}")
    if response.status_code == 200 and ":root" in response.text:
        print("SUCCESS: CSS served.")
    else:
        print(f"FAIL: {response.text[:100]}")

    # 3. JS
    print("\nGET /app/app.js")
    response = client.get("/app/app.js")
    print(f"Status: {response.status_code}")
    if response.status_code == 200 and "init()" in response.text:
        print("SUCCESS: JS served.")
    else:
        print(f"FAIL: {response.text[:100]}")

if __name__ == "__main__":
    test_web()
