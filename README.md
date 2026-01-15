# 📄 Extraction de Documents & Résumé Intelligent (OCR + NLP + NER)

## 🚀 Introduction

Ce projet est une application d’IA permettant :

- de **téléverser une image ou un scan de document** (JPG/PNG),
    
- d’**extraire le texte présent dans l’image (OCR)**,
    
- de **générer automatiquement un résumé** du texte,
    
- et d’**identifier des entités clés** comme les noms propres, lieux, dates…
    

Elle s’appuie sur les librairies :

- **paddleOCR** pour la reconnaissance de caractères,
    
- **Hugging Face Transformers** pour la NER,
  
- **Groq** pour le résumé automatique avec llama
    
- **Pillow** pour la manipulation des images,
    
- **PyTorch** pour l’inférence des modèles IA.
    

---

## 🧠 Schéma Fonctionnel

1️⃣ L’utilisateur envoie une image JPG/PNG  
2️⃣ L’image est convertie en texte par OCR (Tesseract)  
3️⃣ Le texte est :

- résumé via un modèle de summarization
    
- analysé via Named Entity Recognition  
    4️⃣ Le résultat est renvoyé à l’utilisateur  
    5️⃣ L’historique document/résumé peut être sauvegardé
    

---

# 📦 Installation du Projet

## 1️⃣ Cloner le projet

```bash
git clone https://github.com/ElvexDom/Summarize_AI.git
cd Summarize_AI
```

---

## 2️⃣ Création d’un environnement virtuel

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Mac / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3️⃣ Installation des dépendances Python

### Option A : via `requirements.txt`

```bash
pip install -r requirements.txt
```

### Option B : installer librairie par librairie

```bash
pip install paddlepaddle==3.2.2
pip install paddleocr==3.3.2
pip install uvicorn fastapi
pip install torch
pip install transformers
pip install gradio
pip install loguru
pip install bcrypt
pip install groq
```
---

# 📂 Structure du Projet

```
Summarize_AI/
│
├── app/                           # Interface utilisateur (ex: Gradio)
│   ├── __init__.py
│   └── __main__.py                # Point d’entrée principal
│
├── apis/                          # APIs Backend
│   ├── __init__.py
│
│   ├── ia_api/                    # API Intelligence Artificielle
│   │   ├── __init__.py
│   │   └── nlp_api.py             # OCR + résumé + NER
│
│   └── data_api/                  # API de gestion des données
│       ├── __init__.py
│       └── core_api.py            # Stockage utilisateurs & historiques
│
├── services/                      # Logique NLP (HuggingFace)
│   ├── __init__.py
│   └── nlp_service.py
│
├── utils/                         # Utilitaires d’images, conversions
│   ├── __init__.py
│   └── image_utils.py
│
├── models/                        # Stockage / base de données
│   ├── __init__.py
│   └── database.py
│
├── tests/                         # Tests unitaires et validation
│   ├── test_nlp_api.py
|   ├── test_log_watcher.py
│   └── test_data_api.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🖥️ Utilisation

## 1️⃣ Lancer l’interface utilisateur (Front / Gradio)

Depuis la racine du projet :

```bash
python -m app
```

L’interface s’ouvre dans le navigateur → vous pouvez téléverser une image et obtenir :

- le texte OCR,
    
- le résumé,
    
- les entités nommées,
    
- et l’option d’enregistrer l’historique.
    

---

## 2️⃣ Lancer l’API IA (OCR + Résumé + NER) indépendamment

```bash
python -m apis.ia_api.ocr_api
```

📌 Cela permet :

- d’appeler les fonctions IA dans d’autres scripts Python,
    
- ou via HTTP si vous ajoutez FastAPI plus tard.
    

---

## 3️⃣ Lancer l’API Data (historique + utilisateurs) séparément

```bash
python -m apis.data_api.core_api
```

📌 Utile pour :

- gérer l’historique,
    
- brancher une base de données,
    
- tester le backend indépendamment du front.
    

---

# 🧩 Architecture Fonctionnelle Visuelle

```
          Interface Utilisateur (Gradio)
                      │
                      ▼
             ┌─────────────────┐
             │      Nlp API     │
             │ (OCR + LLM + NER)│
             └─────────────────┘
                      │
        texte brut/sollicitation NLP
                      │
                      ▼
             ┌─────────────────┐
             │     Core API     │
             │ (users + history)│
             └─────────────────┘
                      │
         sauvegarde dans modèle/local DB
                      │
                      ▼
                 Fichiers / DB
```

---

# 🎮 Commandes Complètes de Lancement

Depuis la racine du projet :

### 🟢 Démarrer tout ensemble (mode application)

```bash
python -m app
```

### 🔵 Lancer l’IA seule

```bash
python -m apis.ia_api.nlp_api
```

### 🟡 Lancer la Data API seule

```bash
python -m apis.data_api.core_api
```

---

# 📌 Notes Importantes

- Aucun composant ne dépend d’un serveur externe → tout tourne localement
    
- Les APIs Python sont modulaires → tu peux les remplacer ou distribuer
    
- Le front peut appeler les APIs par import local ou par HTTP (si tu ajoute FastAPI plus tard)
    

---

# 🌟 Exemple d’imports depuis `app/__main__.py`

```python
from apis.ia_api.nlp_api import run_ocr, run_summarization, run_ner
from apis.data_api.core_api import save_history, list_documents
```