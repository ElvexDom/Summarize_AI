# services/nlp_service.py
from transformers import pipeline
import re
from tests.paddleocr_script import ocr_image_to_json
import json
from groq import Groq
from dotenv import load_dotenv
import os
import torch


class nlp_serv:
    def __init__(self):
        
        device = 0 if torch.cuda.is_available() else -1
        self.ner = pipeline(
            "ner",
            model="Davlan/bert-base-multilingual-cased-ner-hrl",
            aggregation_strategy="simple",
            device=device,  # FORCER CPU
        )
        
        
        load_dotenv()

        # Charge la clé API GROQ depuis les variables d'environnement. 
        try:
            GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        except:
            print("La clé API GROQ n'a pas été trouvée dans les variables d'environnement.")
            exit()
            
        self.groq_client = Groq(
            api_key=GROQ_API_KEY
        )
        

    def run_summarization(self, text: str) -> str | None:
        """
        Fonction de résumé automatique.
        Pour l'instant, retourne une chaîne vide ou le texte inchangé.
        """
        if not text.strip():
            return ""
        
        system_prompt = {
            "role" : "system",
            "content" : """
                            Tu est un expert en analyse de documents et en synthèse d'informations
                            avec une grande capacité à distinguer les éléments essentiels et non essentiels d'un document.

                            Tu vas analyser un texte qui a été extrait par un modèle OCR d'un document et en faire une synthèse.
                            
                            tu vas renvoyer uniquement le résumé du document fourni, rien d'autre

                        """
                        
        }
        
        user_message = {
            "role" : "user",
            "content" : text
        }
        

        summary_completion = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                system_prompt,
                user_message
            ],
            temperature=0.2
        )
        
        
        
        summary = summary_completion.choices[0].message.content
        # print(summary)
        
        return summary

    
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
