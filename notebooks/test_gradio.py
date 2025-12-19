import gradio as gr
import easyocr
from transformers import pipeline
import cv2
import re

# =======================
# MODELS (chargés 1 fois)
# =======================

# EasyOCR
reader = easyocr.Reader(['fr', 'en'], gpu=False)

# RoBERTa / XLM-RoBERTa pour NER
ner = pipeline(
    "ner",
    model="xlm-roberta-large-finetuned-conll03-english",
    aggregation_strategy="simple"
)

# =======================
# IMAGE PREPROCESSING
# =======================

def preprocess_image(image_path, max_size=1200):
    img = cv2.imread(image_path)

    h, w = img.shape[:2]
    scale = max_size / max(h, w)
    if scale < 1:
        img = cv2.resize(img, (int(w * scale), int(h * scale)))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(gray)

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
        f"{e['word']} → {e['entity']}"
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

demo.launch(share=True)
