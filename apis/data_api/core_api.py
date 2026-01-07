#backend/BD_api.py
import uvicorn
import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

from services.db_tools import initialize_db, read_db, write_user_db, write_resume_db,read_resume_by_user_id
from utils.encode import Encode
encoder = Encode()

#Modèle pydantic
class UserRequest(BaseModel): 
    pseudo : str  
    password : str

class ResumeRequest(BaseModel): 
    user_id: int
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
    """Ajouter un nouvel utilisateur. """

    encode_password = encoder.chiffrer_message(user.password)
    user_data = {"pseudo": user.pseudo,
            "password": encode_password}
    
    write_user_db([user_data])
    
    # #Lecture pour récup l'id (optionnel -> juste pour l'affichage)
    # df = read_db()
    # last_user = df[df.pseudo == user.pseudo]
    return {"succes": True, "message": "Utilisateur ajouté"}



@app.post("/add_resume/")
def add_resume(resume : ResumeRequest):
    write_resume_db(
        user_id=resume.user_id,
        data=[{"name": resume.name, "text": resume.text}]
    )
    return {"succes": True, "message": "Résumé ajouté et Summary mis à jour"}

@app.get("/get_resume/user/{user_id}")
def get_resume_by_id(user_id: int) :
    try:
        
        df = read_resume_by_user_id(user_id)
    
        return df
    except Exception as e:
        return {"error": str(e)}




if __name__ == "__main__":
    # Lancement du serveur pour le développement
    uvicorn.run(
        "apis.data_api.core_api:app",  # Chemin vers le module de l'application
        host="127.0.0.1",
        port=8001,
        reload=True  # Recharge automatique pour le dev, à désactiver en prod
    )