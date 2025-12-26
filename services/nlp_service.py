# services/nlp_service.py
from transformers import pipeline
import re
from tests.paddleocr_script import ocr_image_to_json
import json

class nlp_serv:
    def __init__(self):
        self.ner = pipeline("ner", model="camembert-base", aggregation_strategy="simple")


    def run_summarization(self, text: str) -> str:
        """
        Fonction de résumé automatique.
        Pour l'instant, retourne une chaîne vide ou le texte inchangé.
        """
        # TODO : implémenter le résumé avec HuggingFace
        return ""

    
    def clean_text(self, text):
        text = re.sub(r"\s+", " ", text)
        return text.strip()

 
    def run_ner(self, text: str) -> dict:
        """
        Fonction de reconnaissance d'entités nommées (NER).
        Pour l'instant, retourne un dictionnaire vide.
        """
        if not text.strip():
            return ""
        json_text = json.loads(text)
        all_texts = []
        for page in json_text['text']['results']:
            for line in page['texts']:
                all_texts.append(line['text'])
        text = self.clean_text(text)
        entities = self.ner(all_texts)

        return entities

        # return "\n".join(
        #     f"{e['word']} → {e.get('entity_group', e.get('entity'))}"
        #     for e in entities
        # )
    


    def run_ocr(self, image_byte: bytes):
        """Permet de lire les caractères d'une image."""
        return ocr_image_to_json(image_byte)
