# main.py
import os
from dotenv import load_dotenv
from app.api_client import FastAPIClient
from app.ui.gradio_ui import GradioUI
from utils.log_watcher import LogWatcher

def main():
    """
    Point d'entrée principal de l'application Summarize AI.

    Cette fonction réalise les étapes suivantes :
    1. Charge les variables d'environnement depuis le fichier .env
    2. Initialise les clients API pour l'utilisateur et le pipeline
    3. Crée l'interface Gradio
    4. Lance l'interface Gradio avec logging du démarrage et de la fermeture
    """
    try:
        # --------------------------
        # Charger les variables d'environnement
        # --------------------------
        load_dotenv()
        user_api_base = os.getenv("USER_API_BASE", "http://localhost:8001")
        pipeline_api_base = os.getenv("API_PIPELINE_BASE", "http://localhost:8002")

        # --------------------------
        # Initialiser les clients API
        # --------------------------
        user_api = FastAPIClient.User(user_api_base)
        pipeline_api  = FastAPIClient.Pipeline(pipeline_api_base)

        # --------------------------
        # Créer l'interface Gradio
        # --------------------------
        gradio = GradioUI(user_api, pipeline_api)

        # --------------------------
        # Lancer l'application avec logging
        # --------------------------
        LogWatcher.log("info", "Démarrage de l'application.", screen=True)
        gradio.ui.launch(share=False, debug=False)

    except Exception as e:
        # Log toute erreur inattendue
        LogWatcher.log("error", f"Erreur critique lors du lancement : {e}", screen=True)
        raise  # on relance pour ne pas masquer l'erreur
    finally:
        # Assure un log même si l'application se ferme de manière inattendue
        LogWatcher.log("info", "Fermeture de l'application.", screen=True)


if __name__ == "__main__":
    main()
