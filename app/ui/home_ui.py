import gradio as gr
from gradio.components import Component
from app.ui.resume_ui import ResumeUI
from app.ui.pipeline_ui import PipelineUI

class HomeUI:
    """ui principale visible après login"""

    def __init__(self, user_api: object, pipeline_api: object, user: Component):
        self.user_api = user_api
        self.pipeline_api = pipeline_api
        self.user = user

        # Construire l'UI dès l'initialisation
        self._build()

    # ---- Méthode interne pour construire l'UI ----
    def _build(self):
        """Crée la ui HomeUI dans le contexte Blocks"""
        with gr.Column(visible=False) as self.ui:
            gr.Markdown()
            with gr.Row():
                self.welcome = gr.Markdown("")
                gr.Markdown()
                self.btn_logout = gr.Button("🚪 Déconnexion", variant="stop", size="sm")

            with gr.Tabs():
                with gr.Tab("📄 Générer"):
                    self.pipeline = PipelineUI(self.user_api, self.pipeline_api, self.user)

                with gr.Tab("🔍 Rechercher", id="resume_tab"):
                    self.resume = ResumeUI(self.user_api, self.user)

    # ---- Affichage / Masquage ----
    def show(self) -> gr.update:
        return gr.update(visible=True)

    def hide(self) -> gr.update:
        return gr.update(visible=False, value=None)
