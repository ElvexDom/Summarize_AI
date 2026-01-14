# app/api_client.py
import requests
from pathlib import Path
import pandas as pd


class FastAPIClient:

    # ========================================
    # PIPELINE
    # ========================================
    class Pipeline:
        def __init__(self, base_url: str):
            self.base_url = base_url.rstrip("/")

        # ---- OCR ----
        def fetch_ocr(self, image_path: str) -> str:
            try:
                image_bytes = Path(image_path).read_bytes()
                files = {"file": ("image.jpg", image_bytes, "image/jpeg")}

                response = requests.post(
                    f"{self.base_url}/process_document/",
                    files=files,
                    timeout=60
                )
                response.raise_for_status()
                data = response.json()

                if not data.get("success"):
                    return ""

                pages = []
                for page in data["text"]["results"]:
                    pages.append("\n".join(line["text"] for line in page["texts"]))
                return "\n".join(pages)

            except (requests.RequestException, FileNotFoundError) as e:
                print(f"[PIPELINE OCR] {e}")
                return ""

        # ---- NER ----
        def fetch_ner(self, text: str) -> str:
            try:
                response = requests.post(
                    f"{self.base_url}/ner_text/",
                    json={"text": text},
                    timeout=60
                )
                response.raise_for_status()
                data = response.json()
                return data.get("text", "") if data.get("success") else ""

            except requests.RequestException as e:
                print(f"[PIPELINE NER] {e}")
                return ""

        # ---- RESUME ----
        def fetch_resume(self, text: str) -> str:
            try:
                response = requests.post(
                    f"{self.base_url}/resume_text/",
                    json={"text": text},
                    timeout=60
                )
                response.raise_for_status()
                data = response.json()
                return data.get("text", "") if data.get("success") else ""

            except requests.RequestException as e:
                print(f"[PIPELINE RESUME] {e}")
                return ""

    # ========================================
    # USER
    # ========================================
    class User:
        def __init__(self, base_url: str):
            self.base_url = base_url.rstrip("/")

        # ---- ADD USER ----
        def fetch_add_user(self, username: str, password: str) -> bool:
            try:
                response = requests.post(
                    f"{self.base_url}/add_user/",
                    json={"pseudo": username, "password": password},
                    timeout=5
                )
                response.raise_for_status()
                data = response.json()
                return bool(data.get("success"))

            except requests.RequestException as e:
                print(f"[USER ADD] {e}")
                return False

        # ---- LOGIN USER ----
        def fetch_login_user(self, username: str, password: str) -> dict:
            try:
                response = requests.post(
                    f"{self.base_url}/login/",
                    json={"pseudo": username, "password": password},
                    timeout=5
                )
                response.raise_for_status()
                return response.json()

            except requests.RequestException as e:
                print(f"[USER LOGIN] {e}")
                return {}

        # ---- DELETE USER ----
        def delete_user(self, user_id: int) -> bool:
            try:
                response = requests.delete(
                    f"{self.base_url}/user/{user_id}",
                    timeout=5
                )
                response.raise_for_status()
                data = response.json()
                return bool(data.get("success"))

            except requests.RequestException as e:
                print(f"[USER DELETE] {e}")
                return False

        # ---- SAVE RESUME ----
        def save_resume_to_db(self, resume_name: str, resume_text: str, user: str) -> str:
            try:
                response = requests.post(
                    f"{self.base_url}/add_resume/",
                    json={"user_id": user['id'], "name": resume_name, "text": resume_text},
                    timeout=5
                )
                response.raise_for_status()
                data = response.json()
                if data.get("success"):
                    return f"✅ Résumé '{resume_name}' sauvegardé avec succès."
                return f"❌ Échec de la sauvegarde du résumé '{resume_name}'."

            except requests.RequestException as e:
                print(f"[PIPELINE SAVE RESUME] {e}")
                return f"❌ Erreur lors de la sauvegarde du résumé '{resume_name}'."

        # ---- FETCH READ RESUME ----
        def fetch_read_resume(self, user: str) -> pd.DataFrame:
            try:
                response = requests.get(
                    f"{self.base_url}/get_resume/{user['id']}",
                    timeout=5
                )
                response.raise_for_status()
                data = response.json()
                if data.get("success") and "resumes" in data:
                    return pd.DataFrame(data.get("resumes", []))
                return pd.DataFrame(columns=["id", "resume_name", "resume"])

            except requests.RequestException as e:
                print(f"[USER FETCH RESUME] {e}")
                return pd.DataFrame()

        # ---- DELETE RESUME ----
        def delete_resume(self, resume_id: int) -> bool:
            """
            Supprime un résumé côté API.
            Retourne True si la suppression a réussi, False sinon.
            """
            try:
                response = requests.delete(
                    f"{self.base_url}/delete_resume/{resume_id}",
                    timeout=5
                )
                response.raise_for_status()
                data = response.json()
                success = bool(data.get("success"))
                return success

            except requests.RequestException as e:
                print(f"[USER DELETE] {e}")
                return False
