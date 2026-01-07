# app/ui/inscription_ui.py

import gradio as gr
from app.api_client import FastAPIClient
from app.backend_service import BackendService

# =======================
# Client + BackendService
# =======================
user_api_client = FastAPIClient("http://localhost:8001")
backend_service = BackendService(user_api_client)

def create_login_ui():
    connected = gr.State(False)

    with gr.Column(elem_id="modale-login") as login_ui:
        with gr.Row():
            pseudo_input = gr.Textbox(label="👤 Pseudo", scale=2)
            mdp_input = gr.Textbox(label="🔒 Mot de passe", type="password", scale=2)

        with gr.Row():
            btn_login = gr.Button("🚀 Me connecter", variant="primary", scale=1)
            btn_login.click(backend_service.fetch_login_user, inputs=[pseudo_input, mdp_input], outputs=[connected])
            # btn_inscription = gr.Button("➕ M'inscrire", variant="secondary", scale=1)

    return login_ui
