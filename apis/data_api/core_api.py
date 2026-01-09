#backend/BD_api.py
import uvicorn
import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import bcrypt
load_dotenv()

from services.db_tools import initialize_db, read_db, write_user_db, write_resume_db,read_resume_by_user_id, delete_user_db,delete_resume_by_user_db,find_user_by_pseudo
from utils.encode import Encode
encoder = Encode()

#Modèle pydantic
class UserRequest(BaseModel): 
    pseudo : str  
    password : str

class ResumeRequest(BaseModel):
    user_id: int
    name: str
    text: str

class UserResponse(BaseModel): 
    id : int
    pseudo : str
    class Config:
        from_attributes = True  # Permet de valider depuis les objets SQLAlchemy

class IDresponse(BaseModel):
    id : int

class ResumeResponse(BaseModel):
    id: int
    resume_name: str
    resume: str

    class Config:
        from_attributes = True  # Permet de valider depuis les objets SQLAlchemy

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

    # encode_password = encoder.chiffrer_message(user.password)
    encode_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
    user_data = {"pseudo": user.pseudo,
            "password": encode_password}
    
    write_user_db([user_data])
    
    # #Lecture pour récup l'id (optionnel -> juste pour l'affichage)
    # df = read_db()
    # last_user = df[df.pseudo == user.pseudo]
    return {"succes": True, "message": "Utilisateur ajouté"}



@app.post("/add_resume/")
def add_resume(resume: ResumeRequest):
    """Ajouter un nouveau résumé pour un utilisateur."""
    write_resume_db(
        user_id=resume.user_id,
        data=[{"name": resume.name, "text": resume.text}]
    )
    return {"succes": True, "message": "Résumé ajouté et Summary mis à jour"}


@app.delete("/delete_user/{user_id}")
def delete_user(user_id: int):
    """Supprimer un utilisateur et tous ses résumés associés."""
    if delete_user_db(user_id):

        return {"succes": True, "message": "L'utilisateur a été supprimé avec succès"}
    else:
        return {"succes": False, "message": "L'utilisateur n'a pas pu être supprimé"}
    
@app.delete("/delete_resume/{resume_id}")
def delete_resume(resume_id: int):
    """Supprimer un résumé spécifique par son ID."""
    if delete_resume_by_user_db(resume_id):

        return {"succes": True, "message": "Le résumé a été supprimé avec succès"}
    else:
        return {"succes": False, "message": "Le résumé n'a pas pu être supprimé"}



@app.get("/get_resume/{user_id}")
def get_resume_by_id(user_id: int):
    try:
        df = read_resume_by_user_id(user_id)
        
        # On convertit le DF en liste de dictionnaires
        # 'records' donne : [{"resume_name": "...", "resume": "..."}, ...]
        resumes_list = df.to_dict(orient='records')
        
        return {
            "success": True,
            "resumes": resumes_list
        }
    except Exception as e:
        return {
            "success": False, 
            "error": str(e),
            "resumes": []
        }

@app.post("/login/")
def login(user: UserRequest):
    """Authentifier un utilisateur (à implémenter)."""
    user_found = find_user_by_pseudo(user.pseudo)
    
    if not user_found:
        return {"succes": False, "message"  : "Pseudo ou mot de passe incorrect "} 
    
    if bcrypt.checkpw(user.password.encode('utf-8'),user_found.password.encode('utf-8')): 
        return {"succes": True, "message": "vous etes bien connecté", "data":UserResponse.model_validate(user_found)}  
    
        







if __name__ == "__main__":
    # Lancement du serveur pour le développement
    uvicorn.run(
        "apis.data_api.core_api:app",  # Chemin vers le module de l'application
        host="127.0.0.1",
        port=8001,
        reload=True  # Recharge automatique pour le dev, à désactiver en prod
    )