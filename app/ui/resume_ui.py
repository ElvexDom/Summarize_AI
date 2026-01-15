# app/ui/resume_ui.py
import gradio as gr
from app.api_client import FastAPIClient

class ResumeUI:
    # ========================================
    # SECTION "RÉSUMÉ" : INITIALISATION
    # ========================================
    def __init__(self, user_api: FastAPIClient.User, user: gr.State):
        self.user_api = user_api
        self.user = user
        self.id_resume = gr.State(None)
        self.resumes_list = []  # Stocke localement les résumés récupérés

        # Construire l'UI dès l'initialisation
        self._build()

    # ========================================
    # CONSTRUCTION DE L'UI
    # ========================================
    def _build(self):
        with gr.Column() as self.ui:
            gr.Markdown("## 📝 Mes Résumés")

            # Buttons
            self.btn_fetch = gr.Button("Afficher mes résumés", variant="primary")
            self.btn_delete = gr.Button("Supprimer", variant="primary")

            # Tableau et affichage
            self.data_table = gr.DataFrame(
                value=[],  # initialement vide
                headers=["id", "resume_name", "resume"],
                interactive=False,
                label="Cliquez sur une ligne pour lire le résumé"
            )

            self.display_area = gr.Markdown("### Détails du résumé sélectionné")

            # ---- Logique des boutons ----
            self.btn_fetch.click(
                fn=self.fetch_and_update_table,
                inputs=[self.user],
                outputs=[self.data_table],
                show_progress=False
            )

            # ---- Supprimer et mettre à jour le tableau localement ----
            self.btn_delete.click(
                fn=self.delete_selected_resume,
                inputs=[self.data_table, self.id_resume, self.user],
                outputs=[self.data_table, self.id_resume, self.display_area],
                show_progress=False
            )

            # ---- Callback tableau ----
            self.data_table.select(
                fn=self.update_and_show,
                inputs=[self.data_table],
                outputs=[self.id_resume, self.display_area]
            )

    # ========================================
    # FETCH ET MISE À JOUR DU TABLEAU
    # ========================================
    def fetch_and_update_table(self, user):
        """Récupère les résumés depuis l'API et met à jour le tableau."""
        self.resumes_list = self.user_api.fetch_read_resume(user)

        # Transformer la liste de dicts en liste de listes pour Gradio
        table_data = [
            [r.get("id"), r.get("resume_name"), r.get("resume")]
            for r in self.resumes_list
        ]

        return table_data

    # ========================================
    # CALLBACK POUR AFFICHER UN RÉSUMÉ
    # ========================================
    def update_and_show(self, table_data, evt: gr.SelectData):
        """
        Met à jour l'ID du résumé sélectionné et retourne son contenu.
        Adapté pour table_data en DataFrame.
        """
        try:
            if not evt.index or len(evt.index) == 0:
                return None, "⚠️ Aucune ligne sélectionnée"

            row_index = evt.index[0]

            if row_index >= len(table_data):
                return None, "⚠️ Index hors limites"

            # Accéder à la ligne correctement dans un DataFrame
            selected = table_data.iloc[row_index]

            # Forcer types
            id_resume = int(selected["id"]) if selected["id"] is not None else None
            name = str(selected["resume_name"]) if selected["resume_name"] else "NULL_TEXT_EMPTY"
            text = str(selected["resume"]) if selected["resume"] else "NULL_TEXT_EMPTY"

            display = f"## 📄 {name}\n\n{text}"
            return id_resume, display

        except Exception as e:
            print(f"Erreur update_and_show: {e}")
            return None, f"⚠️ Erreur d'affichage : {str(e)}"

    # ========================================
    # SUPPRIMER UNE LIGNE DANS LE TABLEAU
    # ========================================
    def delete_selected_resume(self, table_data, id_resume, user):
        """
        Supprime le résumé localement après suppression côté API
        et réinitialise la sélection et l'affichage.
        """
        try:
            if id_resume is None:
                return table_data, None, "### Détails du résumé sélectionné"

            # Appel API pour supprimer
            success = self.user_api.delete_resume(id_resume)
            if success:
                # Supprimer la ligne dans le DataFrame
                table_data = table_data[
                    table_data["id"] != id_resume
                ].reset_index(drop=True)

                self.resumes_list = table_data

            # 💖 reset obligatoire après suppression
            return table_data, None, "### Détails du résumé sélectionné"

        except Exception as e:
            print(f"Erreur delete_selected_resume: {e}")
            return table_data, None, "⚠️ Erreur lors de la suppression"

    # ========================================
    # AFFICHAGE / MASQUAGE DE LA SECTION
    # ========================================
    def show(self) -> gr.update:
        return gr.update(visible=True)

    def hide(self) -> gr.update:
        return gr.update(visible=False, value=None)




