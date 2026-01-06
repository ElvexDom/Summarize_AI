# app/frontend_gradio.py  (ou mieux app/ui/nlp_pipeline_ui.py)

import gradio as gr
from app.api_client import FastAPIClient
from app.backend_service import BackendService

# =======================
# Client + BackendService
# =======================
ocr_api_client = FastAPIClient("http://localhost:8002")
backend_service = BackendService(ocr_api_client)

# =======================
# Interface Gradio
# =======================
def create_nlp_pipeline_ui():
    """Retourne l'UI Gradio pour OCR → Résumé → NER"""
    with gr.Blocks() as nlp_ui:
        gr.Markdown("## 📄 NLP Pipeline : OCR → Résumé → NER")
        gr.Markdown(
            "1️⃣ Charge une image et récupère le texte\n"
            "2️⃣ Résume le texte OCR\n"
            "3️⃣ Détecte les entités (NER) dans le texte OCR"
        )

        with gr.Row():
            image_input = gr.Image(type="filepath", label="Image (facture / document)", height=250)

        ocr_textbox = gr.Textbox(label="Texte OCR (modifiable)", lines=15)
        ocr_button = gr.Button("📄 Extraire le texte (OCR)")
        ocr_button.click(fn=backend_service.fetch_ocr, inputs=image_input, outputs=ocr_textbox)

        resume_textbox = gr.Textbox(label="Résumé (modifiable)", lines=5)
        resume_button = gr.Button("📄 Résume le texte (NLP)")
        resume_button.click(fn=backend_service.fetch_resume, inputs=ocr_textbox, outputs=resume_textbox)

        entities_textbox = gr.Textbox(label="Entités détectées (RoBERTa)", lines=15)
        ner_button = gr.Button("🔍 Détecter les entités (NER)")
        ner_button.click(fn=backend_service.fetch_ner, inputs=ocr_textbox, outputs=entities_textbox)

    return nlp_ui
