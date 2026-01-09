import gradio as gr
from app.api_client import FastAPIClient

class PipelineUI:
    def __init__(self, user_client: FastAPIClient.User, pipeline_client: FastAPIClient.Pipeline):
        """
        UI pour le pipeline : OCR → Résumé → NER
        """
        self.user_client = user_client
        self.pipeline_client = pipeline_client
        self.pipeline_ui = None

    def create(self):
        """
        Crée l'UI Gradio pour le pipeline
        """
        with gr.Column() as pipeline_ui:
            self.pipeline_ui = pipeline_ui
            gr.Markdown("## 📄 Pipeline : OCR → Résumé → NER")
            gr.Markdown(
                "1️⃣ Charge une image et récupère le texte\n"
                "2️⃣ Résume le texte OCR\n"
                "3️⃣ Détecte les entités (NER) dans le texte OCR"
            )

            # ---------------- INPUT IMAGE ----------------
            with gr.Row():
                image_input = gr.Image(
                    type="filepath",
                    label="Image (facture / document)",
                    height=250
                )

            # ---------------- OCR ----------------
            ocr_textbox = gr.Textbox(label="Texte OCR (modifiable)", lines=15)
            ocr_button = gr.Button("📄 Extraire le texte (OCR)")
            ocr_button.click(
                fn=self.pipeline_client.fetch_ocr,
                inputs=image_input,
                outputs=ocr_textbox
            )

            # ---------------- RESUME ----------------
            resume_textbox = gr.Textbox(label="Résumé (modifiable)", lines=5)
            resume_button = gr.Button("📄 Résume le texte (PIPELINE)")

            # Ligne avec 3 colonnes : générer résumé, nom + sauvegarde, action sauvegarder
            with gr.Row():
                with gr.Column():
                    # Bouton pour générer le résumé depuis le texte OCR
                    resume_button.click(
                        fn=self.pipeline_client.fetch_resume,
                        inputs=ocr_textbox,
                        outputs=resume_textbox
                    )

                with gr.Column():
                    # Nom du résumé (modifiable)
                    resume_name_textbox = gr.Textbox(
                        label="Nom du résumé (modifiable)",
                        placeholder="Ex: CV_Jean_Dupont",
                        lines=1
                    )
                    save_resume_button = gr.Button("💾 Sauvegarder le résumé")
                    save_status = gr.Markdown()

                with gr.Column():
                    # Action du bouton sauvegarder
                    save_resume_button.click(
                        fn=self.user_client.save_resume_to_db,  # Remplace par backend_service_core si besoin
                        inputs=[resume_name_textbox, resume_textbox],
                        outputs=save_status
                    )

            # ---------------- NER ----------------
            entities_textbox = gr.Textbox(label="Entités détectées (RoBERTa)", lines=15)
            ner_button = gr.Button("🔍 Détecter les entités (NER)")
            ner_button.click(
                fn=self.pipeline_client.fetch_ner,
                inputs=ocr_textbox,
                outputs=entities_textbox
            )

    # ---------------- VISIBILITÉ ----------------
    def delete(self):
        """Supprime complètement le composant UI"""
        return gr.update(visible=False, value=None)
