# app/ui/inscription_ui.py

import gradio as gr
from app.api_client import FastAPIClient
from app.backend_service import BackendService

# =======================
# Client + BackendService
# =======================
user_api_client = FastAPIClient("http://localhost:8001")
backend_service = BackendService(user_api_client)

def create_resume_ui():
    """
    Crée et retourne la modale d'inscription
    """
    with gr.Column(elem_id="modale-inscription") as resume_ui:
        gr.Markdown("## 📝 **A implementer**")