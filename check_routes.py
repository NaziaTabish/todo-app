import requests

try:
    response = requests.get("http://localhost:8000/openapi.json")
    spec = response.json()

    print("API Routes found:")
    for path, methods in spec.get("paths", {}).items():
        print(f"  {path}")

    print("\nLooking for auth routes:")
    auth_paths = [path for path in spec.get("paths", {}) if "auth" in path.lower()]
    for path in auth_paths:
        print(f"  {path}")

except Exception as e:
    print(f"Error: {e}")