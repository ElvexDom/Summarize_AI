# main.py
import os
from dotenv import load_dotenv
from app.api_client import FastAPIClient
from app.ui.gradio_ui import GradioUI
from utils.log_watcher import LogWatcher

def main():
    # --------------------------
    # Charger les variables d'environnement
    # --------------------------
    load_dotenv()
    user_api_url = os.getenv("API_USER_URL", "http://localhost:8001")
    pipeline_api_url  = os.getenv("API_PIPELINE_URL", "http://localhost:8002")

    # --------------------------
    # Initialiser les clients API
    # --------------------------
    user_client = FastAPIClient.User(user_api_url)
    pipeline_client  = FastAPIClient.Pipeline(pipeline_api_url)

    # --------------------------
    # Créer l'interface Gradio
    # --------------------------
    gradio_ui = GradioUI(user_client, pipeline_client)

    # --------------------------
    # Lancer l'application
    # --------------------------
    LogWatcher.log("info", "Démarrage de l'application.", screen=True)
    try:
        gradio_ui.start()
    finally:
        LogWatcher.log("info", "Fermeture de l'application.", screen=True)


if __name__ == "__main__":
    main()
