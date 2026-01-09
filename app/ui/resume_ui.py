# app/ui/resume_ui.py
import gradio as gr
from app.api_client import FastAPIClient

class ResumeUI:
    def __init__(self, user_client: FastAPIClient.User):
        """
        UI pour la section 'Résumé' / User
        """
        self.user_client = user_client
        self.resume_ui = None  # référence à la colonne principale de l'UI

    def create(self):
        """
        Crée la section Resume UI
        """
        with gr.Column(elem_id="modale-resume") as resume_ui:
            self.resume_ui = resume_ui
            gr.Markdown("## 📝 **A implémenter**")
            # Ici tu pourras ajouter les composants : textbox, boutons, affichage résultats, etc.

    def delete(self):
        """
        Supprime complètement le composant Resume UI
        """
        return gr.update(visible=False, value=None)
