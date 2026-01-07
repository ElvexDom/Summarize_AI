#app/backend_service.py

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

    def fetch_add_user(self) -> bool:
        data = self.api.post_json(
            "add_user/",
            {"pseudo":"test", "password":"1234"}
        )

        if data.get("success"):
            return True

        return False