# apis/ia_api/nlp_api.py

"""
Module OCR API
---------------
Ce module expose une API FastAPI permettant :
- Le traitement de documents uploadés via OCR.
- L'extraction d'entités nommées (NER) à partir de texte.
- Des endpoints de monitoring (uptime, version Python/FastAPI, favicon).

Endpoints principaux :
- GET /           : Vérifie le statut de l'API
- GET /favicon.ico: Retourne le favicon
- POST /process_document/ : Traite un document et renvoie le texte OCR
- POST /ner_text/ : Analyse un texte pour extraire les entités nommées
"""

# Librairies standard
from datetime import datetime, timezone  # Gestion des dates et calcul d'uptime
import platform  # Récupération de la version de Python
import importlib.metadata  # Récupération dynamique des versions de packages installés

# Librairies tierces
import uvicorn  # Serveur ASGI pour exécuter FastAPI
from fastapi import FastAPI, UploadFile, File  # Création d'API et gestion des fichiers uploadés
from fastapi.responses import FileResponse  # Pour renvoyer directement des fichiers
from pydantic import BaseModel  # Pour définir des modèles de données validés

# Services personnalisés pour le NLP
from services.nlp_service import nlp_serv  # Fonctions pour résumé et NER

# Initialisation du service NLP
nlp = nlp_serv()

# Création de l'application FastAPI
app = FastAPI(title="IA API", version="1.0")

# Timestamp de démarrage de l'application (UTC) pour calcul d'uptime
start_time = datetime.now(timezone.utc)


class TextRequest(BaseModel):
    """
    Schéma Pydantic pour les requêtes NER.
    Attributs :
    - ocr_text : Texte issu de l'OCR à analyser pour extraire les entités nommées.
    """
    text: str


@app.get("/", include_in_schema=False)
async def root():
    """
    Endpoint principal pour vérifier le statut de l'API.

    Retourne :
    - status : Statut général de l'API
    - time : Heure actuelle en UTC
    - uptime : Temps écoulé depuis le démarrage
    - python_version : Version de Python
    - fastapi_version : Version de FastAPI
    """
    # Calcul de l'uptime
    uptime = datetime.now(timezone.utc) - start_time

    # Tentative de récupération de la version de FastAPI
    try:
        fastapi_version = importlib.metadata.version("fastapi")
    except importlib.metadata.PackageNotFoundError:
        fastapi_version = "unknown"

    return {
        "status": "ok",
        "time": datetime.now(timezone.utc).isoformat(),
        "uptime": str(uptime).split('.')[0],
        "python_version": platform.python_version(),
        "fastapi_version": fastapi_version
    }


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    Endpoint pour renvoyer l'icône du site.
    Utilisé par les navigateurs pour afficher le favicon.
    """
    return FileResponse("static/favicon.png")


@app.post("/process_document/")
async def process_document(file: UploadFile = File(...)):
    """
    Endpoint pour traiter un document uploadé via OCR.

    Paramètres :
    - file : Fichier uploadé (PDF, TXT, etc.)

    Retourne :
    - success : Indicateur de succès
    - text : Texte extrait du document via OCR
    """
    # Lecture asynchrone du contenu du fichier
    content = await file.read()

    # Extraction du texte via OCR
    text = nlp.run_ocr(content)

    return {
        "success": True,
        "text": text
    }


@app.post("/ner_text/")
async def ner_text(request: TextRequest):
    """
    Endpoint pour extraire les entités nommées d'un texte.

    Paramètres :
    - request : Objet NerRequest contenant le texte OCR

    Retourne :
    - success : Indicateur de succès
    - text : Résultat de l'analyse NER
    """
    # Analyse NER
    text = nlp.run_ner(request.text)

    return {
        "success": True,
        "text": text
    }
    
    
@app.post("/resume_text/")
async def resume_text(request: TextRequest):
    """
    Endpoint pour résumer le  texte extrait.

    Paramètres :
    - request : Objet TextRequest contenant le texte OCR

    Retourne :
    - success : Indicateur de succès
    - text : Résultat du résumé du texte
    """
    # Resumé du texte
    text = nlp.run_summarization(request.text)

    return {
        "success": True,
        "text": text
    }


if __name__ == "__main__":
    # Lancement du serveur pour le développement
    uvicorn.run(
        "apis.ia_api.ocr_api:app",  # Chemin vers le module de l'application
        host="127.0.0.1",
        port=8002,
        reload=False  # Recharge automatique pour le dev, à désactiver en prod
    )
