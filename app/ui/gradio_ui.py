# app/ui/gradio_ui.py
import gradio as gr
from app.ui.auth_ui import AuthUI
from app.ui.home_ui import HomeUI
from utils.log_watcher import LogWatcher

class GradioUI:
    """Interface Gradio principale pour l'application Summarize AI.

    Gère l'affichage de l'UI d'authentification et de la section principale (HomeUI),
    ainsi que les callbacks login/logout.
    """

    def __init__(self, user_api: object, pipeline_api: object):
        """
        Initialise l'UI Gradio et construit directement tous les composants.

        Args:
            user_api (FastAPIClient.User): Client pour l'API utilisateur
            pipeline_api (FastAPIClient.Pipeline): Client pour l'API pipeline
        """
        self.user_api = user_api
        self.pipeline_api = pipeline_api

        LogWatcher.log("info", "Initialisation de l'interface Gradio...", screen=True)

        # Construire l'UI dès l'initialisation
        self._build()

    # ---- Méthode interne pour construire l'UI ----
    def _build(self):
        """Construit l'interface Gradio complète avec AuthUI et HomeUI."""
        try:
            with gr.Blocks(title="Summarize AI") as self.ui:

                # Header principal
                gr.Markdown("<center><h1><b>📄 Extraction & Résumé</b></h1></center>")

                # AuthUI : construit automatiquement
                self.auth = AuthUI(self.user_api)

                # HomeUI : construit automatiquement
                self.home = HomeUI(self.user_api, self.pipeline_api, self.auth.user)

                LogWatcher.log("info", "Composants AuthUI et HomeUI construits.", screen=True)

                # ---- Callbacks ----
                self.auth.connected.change(
                    self.handle_connection_change,
                    inputs=[self.auth.connected, self.auth.user],
                    outputs=[self.auth.ui, self.home.ui, self.home.welcome]
                )

                # Bouton logout : met connected à False directement
                self.home.btn_logout.click(
                    lambda: False,
                    outputs=[self.auth.connected]
                )
        except Exception as e:
            LogWatcher.log("error", f"Erreur lors de la construction de l'UI : {e}", screen=True)
            raise e

    # ---- Callback pour login / logout ----
    def handle_connection_change(self, connected: bool, user: dict) -> tuple[gr.update, gr.update, str]:
        if connected:
            LogWatcher.log("info", f"Utilisateur '{user['pseudo']}' connecté.", screen=True)
            return self.auth.hide(), self.home.show(), f"### 👤 Bonjour, {user['pseudo']} !"
        else:
            LogWatcher.log("info", "Utilisateur déconnecté.", screen=True)
            return self.auth.show(), self.home.hide(), ""
