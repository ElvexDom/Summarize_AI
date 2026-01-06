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

    def post_file(self, endpoint: str, file_path: str):
        image_bytes = Path(file_path).read_bytes()
        files = {
            "file": ("image.jpg", image_bytes, "image/jpeg")
        }
        response = requests.post(f"{self.base_url}/{endpoint}", files=files)
        response.raise_for_status()
        return response.json()
