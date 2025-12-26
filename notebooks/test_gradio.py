import gradio as gr
import easyocr
from transformers import pipeline
import re
import numpy as np
from PIL import Image, ImageEnhance

# =======================
# MODELS
# =======================

reader = easyocr.Reader(['fr', 'en'], gpu=False)

ner = pipeline(
    "ner",
    model="xlm-roberta-large-finetuned-conll03-english",
    aggregation_strategy="simple"
)

# =======================
# IMAGE PREPROCESSING
# =======================

def preprocess_image(image_path, max_size=1200):
    img = Image.open(image_path).convert("RGB")

    w, h = img.size
    scale = max_size / max(w, h)
    if scale < 1:
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    gray = img.convert("L")
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(2.0)

    return gray, np.array(gray)


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
        return "", None

    img_pil, img_np = preprocess_image(image_path)

    lines = reader.readtext(
        img_np,
        detail=0,
        paragraph=False,
        allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789À-ÿ.,:/- "
    )

    lines = [l for l in lines if len(l.strip()) > 2]
    text = "\n".join(lines)

    return text, img_pil


# =======================
# STEP 2 — NER
# =======================

def run_ner(text):
    if not text.strip():
        return ""

    text = clean_text(text)
    entities = ner(text)

    return "\n".join(
        f"{e['word']} → {e.get('entity_group', e.get('entity'))}"
        for e in entities
    )

# =======================
# GRADIO UI
# =======================

with gr.Blocks() as demo:
    gr.Markdown("## 📄 OCR (EasyOCR) → NER (XLM-RoBERTa)")

    with gr.Row():
        image = gr.Image(type="filepath", label="Image originale", height=250)
        processed_image = gr.Image(label="Image prétraitée", height=250)

    ocr_text = gr.Textbox(label="Texte OCR (modifiable)", lines=15)

    ocr_button = gr.Button("📄 Extraire le texte (OCR)")

    entities_text = gr.Textbox(label="Entités détectées (NER)", lines=15)
    ner_button = gr.Button("🔍 Détecter les entités")
    api_button = gr.Button("test envoi à l'api")

    ocr_button.click(
        fn=run_ocr,
        inputs=image,
        outputs=[ocr_text, processed_image]
    )

    ner_button.click(
        fn=run_ner,
        inputs=ocr_text,
        outputs=entities_text
    )


demo.launch(share=True)
