# app/ui/inscription_ui.py

import gradio as gr

def create_inscription_ui():
    """
    Crée et retourne la modale d'inscription
    """
    with gr.Column(visible=False, elem_id="modale-inscription") as inscription_ui:
        gr.Markdown("## 📝 **Créer un compte**")
        p_reg = gr.Textbox(label="Pseudo")
        m_reg = gr.Textbox(label="Email")
        mdp_reg = gr.Textbox(label="Mot de passe", type="password")
        mdp_c_reg = gr.Textbox(label="Confirmer", type="password")
        
        with gr.Row():
            btn_create = gr.Button("✅ Créer", variant="primary", scale=1)
            btn_close = gr.Button("❌ Fermer", variant="stop", scale=1)
        
        msg_create = gr.Markdown()
    
    # Retourner tous les éléments pour pouvoir brancher les événements
    return inscription_ui, p_reg, m_reg, mdp_reg, mdp_c_reg, btn_create, btn_close, msg_create



# # app/ui/inscription_ui.py

# import gradio as gr
# from app.api_client import FastAPIClient
# from app.backend_service import BackendService

# # =======================
# # Client + BackendService
# # =======================
# user_api_client = FastAPIClient("http://localhost:8001")
# backend_service = BackendService(user_api_client)

# def create_inscription_ui():
#     """
#     Crée et retourne la modale d'inscription
#     """
#     with gr.Column(visible=False, elem_id="modale-inscription") as inscription_ui:
#         gr.Markdown("## 📝 **Créer un compte**")
#         p_reg = gr.Textbox(label="Pseudo")
#         mdp_reg = gr.Textbox(label="Mot de passe", type="password")
#         mdp_c_reg = gr.Textbox(label="Confirmer", type="password")

#         successRequest = False
#         inputRequest = {"pseudo": p_reg, "password": mdp_reg}

#         with gr.Row():
#             btn_create = gr.Button("✅ Créer", variant="primary", scale=1)
#             btn_create.click(fn=backend_service.fetch_add_user, inputs=inputRequest, outputs=successRequest)

#             btn_close = gr.Button("❌ Fermer", variant="stop", scale=1)
        
#         msg_create = gr.Markdown()

#     def test():
#         backend_service.fetch_add_user({"pseudo": p_reg, "password": mdp_reg})
    
#     # Retourner tous les éléments pour pouvoir brancher les événements
#     return inscription_ui, p_reg, mdp_reg, mdp_c_reg, btn_create, btn_close, msg_create
