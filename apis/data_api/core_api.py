#backend/BD_api.py
import uvicorn
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

from services.db_tools import initialize_db, read_db, write_user_db

#Modèle pydantic
class UserRequest(BaseModel): 
    pseudo : str  
    password : str

class ResumeRequest(BaseModel): 
    name : str  
    text : str

class UserResponse(BaseModel): 
    id : int
    pseudo : str

class IDresponse(BaseModel): 
    id : int   

API_ROOT_URL = f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT', '8080')}" 

#--- Création si besoin de la base de données ---
initialize_db()

# --- Configuration ---
app = FastAPI(title='API')

@app.get("/") 
def read_root(): 
    """Vérifie que la root fonctionne."""
    return {"Hello": "world", "status": "API is running"}

@app.post("/add_user/")
def add_user(user : UserRequest):
    """Ajouter un nouvel utilisateur.   DANS LE WRITE METTRE LE CRYPTAGE DU MOT DE PASSE"""
    user_data = {"pseudo": user.pseudo,
            "password": user.password}
    
    write_user_db([user_data])
    
    # #Lecture pour récup l'id (optionnel -> juste pour l'affichage)
    # df = read_db()
    # last_user = df[df.pseudo == user.pseudo]
    return "Utilisateur ajouté."

@app.post("/add_resume/")
def add_resume(resume : ResumeRequest):
    """Ajouter un nouvel utilisateur.   DANS LE WRITE METTRE LE CRYPTAGE DU MOT DE PASSE"""
    resume_data = {"name": resume.name,
            "text": resume.text}
    
    write_db([resume_data])
    
    # #Lecture pour récup l'id (optionnel -> juste pour l'affichage)
    # df = read_db()
    # last_user = df[df.pseudo == user.pseudo]
    return "Utilisateur ajouté."

if __name__ == "__main__":
    # Lancement du serveur pour le développement
    uvicorn.run(
        "apis.data_api.core_api:app",  # Chemin vers le module de l'application
        host="127.0.0.1",
        port=8002,
        reload=True  # Recharge automatique pour le dev, à désactiver en prod
    )