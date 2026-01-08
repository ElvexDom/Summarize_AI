# app/ui/inscription_ui.py

import gradio as gr
from app.api_client import FastAPIClient
from app.backend_service import BackendService
import pandas as pd

# from services.db_tools import read_resume_by_user_id 
# =======================
# Client + BackendService
# =======================
user_api_client = FastAPIClient("http://localhost:8001")
backend_service = BackendService(user_api_client)
fetch_read_resume = backend_service.fetch_read_resume


def create_resume_ui():
    with gr.Column() as resume_ui:
        gr.Markdown("## 📝 Mes Résumés")

        # Composant pour saisir l'ID (ou à cacher si vous avez un système de login)
        user_id_input = gr.Number(label="Votre ID Utilisateur", value=1)
        
        btn_fetch = gr.Button("Afficher mes résumés", variant="primary")

        # LE COMPOSANT D'AFFICHAGE
        data_table = gr.DataFrame(
            headers=["id", "resume_name", "resume"],
            interactive=False,
            label="Cliquez sur une ligne pour lire le résumé"
        )

        # Zone de lecture pour le résumé sélectionné
        display_area = gr.Markdown("### Détails du résumé sélectionné")

        # --- LOGIQUE DES BOUTONS ---

        # Clic pour charger les données
        btn_fetch.click(
            fn=backend_service.fetch_read_resume,
            inputs=[user_id_input], # Envoie l'ID à la fonction
            outputs=[data_table]# Met à jour le TABLEAU
        )

        def show_details(df, evt: gr.SelectData):
            # evt.index contient (row_index, col_index)
            row_index = evt.index[0]
            
            try:
                # On accède aux cellules par leur position (0 = 1ère col, 1 = 2ème col, etc.)
                # Selon votre API : 0 est 'resume_name' et 1 est 'resume'
                name = df.iloc[row_index, 0] 
                text = df.iloc[row_index, 1]
        
                return f"## 📄 {name}\n\n{text}"
            except Exception as e:
                return f"⚠️ Erreur d'affichage : {str(e)}"

        data_table.select(
            fn=show_details,
            inputs=[data_table],
            outputs=[display_area]
        )

    return resume_ui
              