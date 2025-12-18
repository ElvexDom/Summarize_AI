# 📄 Extraction de Documents & Résumé Intelligent (OCR + NLP + NER)

## 🚀 Introduction

Ce projet est une application d’IA permettant :

- de **téléverser une image ou un scan de document** (JPG/PNG),
    
- d’**extraire le texte présent dans l’image (OCR)**,
    
- de **générer automatiquement un résumé** du texte,
    
- et d’**identifier des entités clés** comme les noms propres, lieux, dates…
    

Elle s’appuie sur les librairies :

- **pytesseract** pour la reconnaissance de caractères,
    
- **Hugging Face Transformers** pour le résumé automatique & la NER,
    
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
pip install pytesseract
pip install Pillow
pip install torch
pip install transformers
```

---
