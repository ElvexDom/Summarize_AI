# app/ui/gradio_ui.py
import gradio as gr
from app.api_client import FastAPIClient
from app.ui.auth_ui import AuthUI
from app.ui.resume_ui import ResumeUI
from app.ui.pipeline_ui import PipelineUI
from utils.log_watcher import LogWatcher

class GradioUI:
    def __init__(self, user_client: FastAPIClient.User, pipeline_client: FastAPIClient.Pipeline):
        """
        Initialise l'application Gradio avec les clients API User et Pipeline.
        """
        self.user_client = user_client
        self.pipeline_client = pipeline_client
        self.gradio_ui = None
        self.authUI = None
        self.resumeUI = None
        self.pipelineUI = None

    def create(self):
        """
        Crée la structure de l'interface Gradio
        """
        with gr.Blocks(title="Summarize AI") as self.gradio_ui:
            gr.Markdown("<center><h1><b>📄 Extraction & Résumé</b></h1></center>")

            # -------- SECTION AUTHENTIFICATION --------
            with gr.Column(visible=True) as section_auth:
                self.authUI = AuthUI(user_client=self.user_client)
                self.authUI.create()  # construit l'UI Auth

            # -------- SECTION CONNECTÉE --------
            with gr.Column(visible=False) as section_connecte:
                # Markdown dynamique pour afficher le pseudo
                self.user_label = gr.Markdown("")  
                btn_logout = gr.Button("🚪 Déconnexion", variant="stop")

                with gr.Tabs():
                    # Onglet "Générer" → PipelineUI
                    with gr.Tab("📄 Générer"):
                        self.pipelineUI = PipelineUI(
                            user_client=self.user_client,
                            pipeline_client=self.pipeline_client
                        )
                        self.pipelineUI.create()

                    # Onglet "Rechercher" → ResumeUI
                    with gr.Tab("🔍 Rechercher"):
                        self.resumeUI = ResumeUI(user_client=self.user_client)
                        self.resumeUI.create()

            # -------- GESTION LOGIN / VISIBILITÉ --------
            def on_login(logged, pseudo):
                """
                Après login réussi :
                - cache AuthUI
                - affiche section connectée
                - met à jour le Markdown avec le pseudo
                """
                if logged:
                    return gr.update(visible=False), gr.update(visible=True), f"### 👤 Bonjour, {pseudo} !"
                else:
                    return gr.update(visible=True), gr.update(visible=False), ""

            # Lier le State pseudo et is_logged pour mettre à jour Markdown
            self.authUI.is_logged.change(
                on_login,
                inputs=[self.authUI.is_logged, self.authUI.current_user],
                outputs=[self.authUI.auth_ui, section_connecte, self.user_label]
            )

            # -------- DÉCONNEXION --------
            def logout():
                """
                Cache section connectée, réaffiche AuthUI
                et remet is_logged à False
                """
                return gr.update(visible=True), gr.update(visible=False), False

            btn_logout.click(
                logout,
                outputs=[self.authUI.auth_ui, section_connecte, self.authUI.is_logged]
            )

    def start(self, share: bool = False, debug: bool = False):
        """
        Démarre l'interface Gradio
        """
        if not self.gradio_ui:
            self.create()
        LogWatcher.log("info", "Démarrage de l'interface Gradio...", screen=True)
        self.gradio_ui.launch(share=share, debug=debug)
