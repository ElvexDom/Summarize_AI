# services/nlp_service.py
from transformers import pipeline
import re
from tests.paddleocr_script import ocr_image_to_json
import json

class nlp_serv:
    def __init__(self):
        self.ner = pipeline(
            "ner",
            model="Davlan/bert-base-multilingual-cased-ner-hrl",
            aggregation_strategy="simple",
            device=-1,  # FORCER CPU
        )

        self.summarization = pipeline(
            "summarization",
            model="plguillou/t5-base-fr-sum-cnndm",
            device=-1,  # FORCER CPU
        )
        

    def run_summarization(self, text: str) -> str:
        """
        Fonction de résumé automatique.
        Pour l'instant, retourne une chaîne vide ou le texte inchangé.
        """
        if not text.strip():
            return ""
        
        summary = self.summarization(text)
        
        
        
        print(summary)
        # TODO : implémenter le résumé avec HuggingFace
        return ""

    
    def clean_text(self, text):
        text = re.sub(r"\s+", " ", text)
        return text.strip()

 
    def run_ner(self, text: str) -> dict:
        """
        Fonction de reconnaissance d'entités nommées (NER).
        Retourne un texte formaté "mot → label".
        """
        if not text.strip():
            return ""

        # Nettoyage du texte
        text = self.clean_text(text)

        # Extraction des entités
        entities = self.ner(text)

        # Formattage dans une variable intermédiaire
        formatted_entities = [
            f"{e['word']} → {e.get('entity_group', e.get('entity'))}" 
            for e in entities
        ]

        # Retour sous forme de chaîne unique
        return "\n".join(formatted_entities)
    


    def run_ocr(self, image_byte: bytes):
        """Permet de lire les caractères d'une image."""
        return ocr_image_to_json(image_byte)
