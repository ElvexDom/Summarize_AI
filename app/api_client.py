#app/api_client.py

import requests
from pathlib import Path

class FastAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def post_json(self, endpoint: str, payload: dict):
        response = requests.post(f"{self.base_url}/{endpoint}", json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_json(self, endpoint: str):
        """Envoie une requête GET à l'API et retourne le JSON."""
        try:
            response = requests.get(f"{self.base_url}/{endpoint}")
            response.raise_for_status() # Lève une erreur si 404, 500, etc.
            return response.json()
        except Exception as e:
            print(f"Erreur API Client (GET): {e}")
            return {"success": False, "error": str(e)}

    def post_file(self, endpoint: str, file_path: str):
        image_bytes = Path(file_path).read_bytes()
        files = {
            "file": ("image.jpg", image_bytes, "image/jpeg")
        }
        response = requests.post(f"{self.base_url}/{endpoint}", files=files)
        response.raise_for_status()
        return response.json()
