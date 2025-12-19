import gradio as gr
import easyocr
from transformers import pipeline
import cv2
import re
from PIL import Image, ImageEnhance
import requests
from pathlib import Path


# EasyOCR
reader = easyocr.Reader(['fr', 'en'], gpu=False)

# RoBERTa / XLM-RoBERTa pour NER
ner = pipeline(
    "ner",
    model="xlm-roberta-large-finetuned-conll03-english",
    aggregation_strategy="simple"
)

def fetch_api(image_path):
    url_fastapi = "http://localhost:8002/process_document"

    image_bytes = Path(image_path).read_bytes()

    files = {
        "file": ("image.jpg", image_bytes, "image/jpeg")
    }

    response = requests.post(url_fastapi, files=files)

    return response.text

# =======================
# IMAGE PREPROCESSING
# =======================

def preprocess_image(image_path, max_size=1200):
    # Charger l'image
    img = Image.open(image_path).convert("RGB")

    # Redimensionnement en gardant le ratio
    w, h = img.size
    scale = max_size / max(w, h)
    if scale < 1:
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    # Conversion en niveaux de gris
    gray = img.convert("L")

    # Amélioration du contraste (approximation CLAHE)
    enhancer = ImageEnhance.Contrast(gray)
    contrast = enhancer.enhance(2.0)  # facteur ajustable

    return contrast

# =======================
# TEXT CLEANING
# =======================

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# =======================
# STEP 1 — OCR
# =======================

def run_ocr(image_path):
    if image_path is None:
        return ""

    img = preprocess_image(image_path)

    lines = reader.readtext(
        img,
        detail=0,
        paragraph=False,
        allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789À-ÿ.,:/- "
    )

    lines = [l for l in lines if len(l.strip()) > 2]
    return "\n".join(lines)

# =======================
# STEP 2 — NER
# =======================

def run_ner(text):
    if not text.strip():
        return ""

    text = clean_text(text)
    entities = ner(text)

    return "\n".join(
        f"{e['word']} → {e['entity_group']}"
        for e in entities
    )

# =======================
# GRADIO UI
# =======================

with gr.Blocks() as demo:
    gr.Markdown("## 📄 OCR (EasyOCR) → NER (RoBERTa)")
    gr.Markdown(
        "1️⃣ Charge une image et récupère le texte\n"
        "2️⃣ Clique sur **Détecter les entités** pour lancer le NER"
    )

    with gr.Row():
        image = gr.Image(type="filepath", label="Image (facture / document)", height=250)

    with gr.Row():
        ocr_text = gr.Textbox(label="Texte OCR (modifiable)", lines=15)

    ocr_button = gr.Button("📄 Extraire le texte (OCR)")

    with gr.Row():
        entities_text = gr.Textbox(label="Entités détectées (RoBERTa)", lines=15)

    ner_button = gr.Button("🔍 Détecter les entités (NER)")

    api_button = gr.Button("Envoyer a l api")

    # Actions
    ocr_button.click(
        fn=run_ocr,
        inputs=image,
        outputs=ocr_text
    )

    ner_button.click(
        fn=run_ner,
        inputs=ocr_text,
        outputs=entities_text
    )

    api_button.click(
        fn=fetch_api,
        inputs=image,
        outputs=ocr_text
    )

# demo.launch(share=True)




