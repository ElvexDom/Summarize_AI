#app/backend_service.py
import pandas as pd
class BackendService:
    def __init__(self, api_client):
        self.api = api_client

    # ---------- OCR ----------
    def fetch_ocr(self, image_path: str) -> str:
        data = self.api.post_file("process_document/", image_path)

        if not data.get("success"):
            return ""

        all_pages = []
        for page in data["text"]["results"]:
            page_texts = [line["text"] for line in page["texts"]]
            all_pages.append("\n".join(page_texts))

        return "\n".join(all_pages)

    # ---------- NER ----------
    def fetch_ner(self, text: str) -> str:
        data = self.api.post_json(
            "ner_text/",
            {"text": text}
        )

        if data.get("success"):
            return data["text"]

        return ""

    # ---------- RESUME ----------
    def fetch_resume(self, text: str) -> str:
        data = self.api.post_json(
            "resume_text/",
            {"text": text}
        )

        if data.get("success"):
            return data["text"]

        return ""

    def save_resume_to_db(self, name, text):
        # L'ID de l'utilisateur (à récupérer via un état de session plus tard)
        user_id = 1 

        # Ce dictionnaire sera converti en JSON par requests
        # Les clés 'user_id', 'name' et 'text' doivent être identiques à ResumeRequest
        payload = {
            "user_id": user_id,
            "name": name,
            "text": text
        }

        # On envoie le payload à la route /add_resume/
        response = self.api.post_json("add_resume/", payload)
        
        # Rappel : votre API renvoie "succes" (un seul 's')
        if response.get("succes"):
            return f"✅ {response['message']}"
        
        return f"❌ Erreur : {response.get('message', 'Échec de la sauvegarde')}"
    

    def fetch_add_user(self, username, mdp) -> bool:
        data = self.api.post_json(
            "add_user/",
            {"pseudo":username, "password":mdp}
        )

        if data.get("success"):
            return True

        return False

    def fetch_read_resume(self, user_id: int):
        data = self.api.get_json(f"get_resume/{user_id}")

        if data.get("success"):
            print(data['resumes'])
            return pd.DataFrame(data['resumes'])

        return []

    def fetch_login_user(self, username, mdp) -> bool:
        data = self.api.post_json(
            "login/",
            {"pseudo":username, "password":mdp}
        )

        if data.get("success"):
            return True

        return False