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
                visible=["resume_name", "resume"],
                headers=["id", "resume_name", "resume"],
                interactive=False,
                label="Cliquez sur une ligne pour lire le résumé"
            )

            self.display_area = gr.Markdown("### Détails du résumé sélectionné")

            # ---- Logique des boutons ----
            self.btn_fetch.click(
                fn=self.user_api.fetch_read_resume,
                inputs=[self.user],
                outputs=[self.data_table]
            )

            # ---- Supprimer et mettre à jour le tableau localement ----
            self.btn_delete.click(
                fn=self.delete_selected_resume,
                inputs=[self.data_table, self.id_resume, self.user],
                outputs=[self.data_table]
            )

            # ---- Callback tableau ----
            self.data_table.select(
                fn=self.update_and_show,
                inputs=[self.data_table],
                outputs=[self.id_resume, self.display_area]
            )

    # ========================================
    # CALLBACK POUR AFFICHER UN RÉSUMÉ
    # ========================================
    def update_and_show(self, df, evt: gr.SelectData):
        """
        Met à jour l'ID du résumé sélectionné et retourne son contenu.
        Retour : (id_resume, affichage_markdown)
        """
        row_index = evt.index[0]
        try:
            id_resume = int(df.iloc[row_index, 0])
            name = df.iloc[row_index, 1]
            text = df.iloc[row_index, 2]
            display = f"## 📄 {name}\n\n{text}"
            return id_resume, display
        except Exception as e:
            print(f"Erreur update_and_show: {e}")
            return None, f"⚠️ Erreur d'affichage : {str(e)}"

    # ========================================
    # SUPPRIMER UNE LIGNE DANS LE TABLEAU
    # ========================================
    def delete_selected_resume(self, df, id_resume, user):
        """
        Supprime le résumé localement après suppression côté API.
        """
        if id_resume is None:
            return df  # rien à supprimer

        # Appel API pour supprimer
        success = self.user_api.delete_resume(id_resume)
        if success:
            # Supprime la ligne correspondante dans le DataFrame local
            df = df[df.iloc[:, 0] != id_resume]
        return df

    # ========================================
    # AFFICHAGE / MASQUAGE DE LA SECTION
    # ========================================
    def show(self) -> gr.update:
        return gr.update(visible=True)

    def hide(self) -> gr.update:
        return gr.update(visible=False, value=None)
