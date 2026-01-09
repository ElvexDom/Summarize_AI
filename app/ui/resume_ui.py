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
        self.id_resume = gr.State(None)
        self.deleted_resume = gr.State(False)

    def create(self):
        """
        Crée la section Resume UI
        """
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
            btn_delete = gr.Button("Supprimer", variant="primary")

            # --- LOGIQUE DES BOUTONS ---

            # Clic pour charger les données
            btn_fetch.click(
                fn=self.user_client.fetch_read_resume,
                inputs=[user_id_input], # Envoie l'ID à la fonction
                outputs=[data_table]# Met à jour le TABLEAU
            )

            btn_delete.click(
                fn=self.user_client.delete_resume,
                inputs=[self.id_resume], # Envoie l'ID à la fonction
                outputs=[self.deleted_resume]# Met à jour le TABLEAU
            )

            def update_id(df, evt: gr.SelectData):
                # evt.index contient (row_index, col_index)
                row_index = evt.index[0]

                try:
                    # Récupérer l'id dans la première colonne (col 0)
                    id_resume = int(df.iloc[row_index, 0])
                    return id_resume  # mettra à jour gr.State
                except Exception as e:
                    print(f"Erreur update_id: {e}")
                    return None

            def show_details(df, evt: gr.SelectData):
                # evt.index contient (row_index, col_index)
                row_index = evt.index[0]
                
                try:
                    # On accède aux cellules par leur position (0 = 1ère col, 1 = 2ème col, etc.)
                    # Selon votre API : 0 est 'resume_name' et 1 est 'resume'
                    name = df.iloc[row_index, 1]
                    text = df.iloc[row_index, 2]
            
                    return f"## 📄 {name}\n\n{text}"
                except Exception as e:
                    return f"⚠️ Erreur d'affichage : {str(e)}"

            data_table.select(
                fn=show_details,
                inputs=[data_table],
                outputs=[display_area]
            )

            data_table.select(
                fn=update_id,
                inputs=[data_table],
                outputs=[self.id_resume]
            )

        return resume_ui

    def delete(self):
        """
        Supprime complètement le composant Resume UI
        """
        return gr.update(visible=False, value=None)
