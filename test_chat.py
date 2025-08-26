import requests
import json

# Test de l'endpoint de chat
url = "http://localhost:8000/chat"
data = {
    "message": "Bonjour, comment allez-vous ?",
    "session_id": "test-123"
}

try:
    response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Erreur: {e}")















