#app/frontend_gradio.py

import gradio as gr
from app.api_client import FastAPIClient  # ton client
from app.backend_service import BackendService    # ta classe métier

# Crée le client FastAPI avec l'URL de ton API
ocr_api_client = FastAPIClient("http://localhost:8002")

# Passe ce client à BackendService
backend_service = BackendService(ocr_api_client)

# =======================
# GRADIO UI
# =======================
with gr.Blocks() as gradio:
    gr.Markdown("## 📄 OCR (PaddleOCR) → NER (RoBERTa)")
    gr.Markdown(
        "1️⃣ Charge une image et récupère le texte\n"
        "2️⃣ Résume le texte OCR\n"
        "3️⃣ Détecte les entités (NER) dans le texte OCR"
    )

    with gr.Row():
        image = gr.Image(type="filepath", label="Image (facture / document)", height=250)

    with gr.Row():
        ocr_text = gr.Textbox(label="Texte OCR (modifiable)", lines=15)

    ocr_button = gr.Button("📄 Extraire le texte (OCR)")

    with gr.Row():
        resume_text = gr.Textbox(label="Résumé (modifiable)", lines=5)

    resume_button = gr.Button("📄 Résume le texte (NLP)")

    with gr.Row():
        entities_text = gr.Textbox(label="Entités détectées (RoBERTa)", lines=15)

    ner_button = gr.Button("🔍 Détecter les entités (NER)")

    # =======================
    # Brancher les boutons aux méthodes de BackendService
    # =======================
    ocr_button.click(
        fn=backend_service.fetch_ocr,
        inputs=image,
        outputs=ocr_text
    )

    resume_button.click(
        fn=backend_service.fetch_resume,
        inputs=ocr_text,
        outputs=resume_text
    )

    ner_button.click(
        fn=backend_service.fetch_ner,
        inputs=ocr_text,
        outputs=entities_text
    )
