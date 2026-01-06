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
