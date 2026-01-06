from paddleocr import PaddleOCR
import cv2
import numpy as np

ocr = PaddleOCR(
    lang="fr",                             # langue française
    use_textline_orientation=True,         # corrige l'orientation ligne par ligne
    # use_doc_orientation_classify=True,     # corrige l'orientation globale du document
    # use_doc_unwarping=True,               # redressement des plis/déformations désactivé (plus rapide)
    # text_detection_model_dir="./models/det/PP-OCRv5_server_det",       # modèle détection local
    # text_recognition_model_dir="./models/rec/latin_PP-OCRv5_mobile_rec", # modèle reconnaissance local
    # textline_orientation_model_dir="./models/cls/PP-LCNet_x1_0_textline_ori", # classification lignes texte
    # doc_orientation_classify_model_dir="./models/cls/PP-LCNet_x1_0_doc_ori", # orientation doc
    # doc_unwarping_model_dir="./models/unwarp/UVDoc"                    # redressement plis/déformations
)

def resize_image(img, max_width=1024, max_height=1024):
    h, w = img.shape[:2]
    scale = min(max_width / w, max_height / h, 1)
    new_w, new_h = int(w * scale), int(h * scale)
    return cv2.resize(img, (new_w, new_h))

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

def bytes_to_cv2_image(image_bytes: bytes) -> np.ndarray:
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

def ocr_image_to_json(img_bytes: bytes):
    """Transforme l'image en texte."""
    
    img = bytes_to_cv2_image(img_bytes) #bytes -> np.array
    
    if img is None:
        return {"error": f"Impossible de charger l'image : {img}"}

    #Transformation de l'image
    img = resize_image(img)
    img = preprocess_image(img)

    #Résultat : texte de l'image sous format json
    results = ocr.predict(img)

    output = []
    for page_number, page_result in enumerate(results, start=1):
        texts = page_result.get("rec_texts", [])
        scores = page_result.get("rec_scores", [])
        output.append({
            "page_number": page_number,
            "texts": [
                {"text": text, "score": float(score)}
                for text, score in zip(texts, scores)
            ]
        })

    return {
        "total_pages": len(results),
        "results": output
    }


