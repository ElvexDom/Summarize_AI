# apis/ia_api/ocr_api.py

# Librairies standard
from datetime import datetime, timezone  # Gestion des dates et calcul d'uptime
import platform  # Récupération de la version de Python
import importlib.metadata  # Récupération dynamique des versions de packages installés

# Librairies tierces
import uvicorn  # Serveur ASGI pour exécuter FastAPI
from fastapi import FastAPI, UploadFile, File  # Création d'API et gestion des fichiers uploadés
from fastapi.responses import FileResponse  # Pour renvoyer directement des fichiers (favicon, etc.)

# Services personnalisés pour le NLP
from services.nlp_service import nlp_serv  # Fonctions pour résumé et NER


# Création de l'application FastAPI
app = FastAPI(title="IA API", version="1.0")

# Timestamp de démarrage de l'application (UTC)
start_time = datetime.now(timezone.utc)


@app.get("/", include_in_schema=False)
async def root():
    """
    Endpoint principal pour vérifier le statut de l'API.
    Renvoie :
    - status : statut général de l'API
    - time : heure actuelle UTC
    - uptime : temps écoulé depuis le démarrage
    - python_version : version de Python
    - fastapi_version : version de FastAPI
    """
    uptime = datetime.now(timezone.utc) - start_time  # Calcul de l'uptime
    try:
        fastapi_version = importlib.metadata.version("fastapi")
    except importlib.metadata.PackageNotFoundError:
        fastapi_version = "unknown"

    return {
        "status": "ok",
        "time": datetime.now(timezone.utc).isoformat(),
        "uptime": str(uptime).split('.')[0],  # Formattage pour enlever les microsecondes
        "python_version": platform.python_version(),
        "fastapi_version": fastapi_version
    }


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    Endpoint pour renvoyer l'icône du site.
    """
    return FileResponse("static/favicon.png")  # Retourne le favicon


@app.post("/process_document")
async def process_document(file: UploadFile = File(...)):
    """
    Endpoint pour traiter un document uploadé.
    - file : fichier uploadé (PDF, TXT, etc.)
    Retourne un résumé généré par la logique NLP.
    """
    content = await file.read()  # Lire le contenu du fichier de manière asynchrone

    nlp = nlp_serv()
    text = nlp.run_ocr(content)
    print(text)
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
        reload=True  # Recharge automatique pour le dev, à désactiver en prod
    )
