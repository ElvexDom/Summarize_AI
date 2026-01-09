# API FastAPI pour la gestion des utilisateurs et des résumés
import uvicorn
import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import bcrypt
load_dotenv()

from services.db_tools import (
    initialize_db, 
    write_user_db,
    update_resume_by_id,
    write_resume_db,
    delete_user_db,
    find_user_by_pseudo,
    delete_resume_by_user_db,
    read_resume_by_user_id,
    get_resume_by_id ,
)
# Modèles Pydantic pour les requêtes et réponses
class UserRequest(BaseModel):
    """Modèle pour l'inscription et la connexion d'un utilisateur."""
    pseudo : str
    password : str

class ResumeRequest(BaseModel):
    """Modèle pour l'ajout ou la modification d'un résumé."""
    user_id: int
    name: str
    text: str

class UserResponse(BaseModel):
    """Modèle de réponse contenant les informations d'un utilisateur."""
    id : int
    pseudo : str
    class Config:
        from_attributes = True  # Permet de valider depuis les objets SQLAlchemy

class IDresponse(BaseModel):
    """Modèle de réponse contenant uniquement un ID."""
    id : int

class ResumeResponse(BaseModel):
    """Modèle de réponse contenant les informations d'un résumé."""
    id: int
    resume_name: str
    resume: str

    class Config:
        from_attributes = True  # Permet de valider depuis les objets SQLAlchemy

API_ROOT_URL = f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT', '8080')}"

# Création de la base de données si elle n'existe pas
initialize_db()

# Configuration de l'application FastAPI
app = FastAPI(title='API')

@app.get("/")
def read_root():
    """Endpoint de vérification de l'état de l'API.

    Returns:
        dict: Message de statut confirmant que l'API est opérationnelle.
    """
    return {"Hello": "world", "status": "API is running"}

@app.post("/add_user/")
def add_user(user : UserRequest):
    """Créer un nouvel utilisateur avec mot de passe hashé.

    Args:
        user (UserRequest): Informations de l'utilisateur (pseudo et mot de passe).

    Returns:
        dict: Statut de succès et message.
    """
    # Hashage du mot de passe avec bcrypt
    encode_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
    user_data = {"pseudo": user.pseudo,
            "password": encode_password}
    
    write_user_db([user_data])
    
    # #Lecture pour récup l'id (optionnel -> juste pour l'affichage)
    # df = read_db()
    # last_user = df[df.pseudo == user.pseudo]
    return {"success": True, "message": "Utilisateur ajouté"}

@app.patch("/resume/{resume_id}")
def update_resume(resume_id: int, resume: ResumeRequest):
    """Modifier un résumé existant.

    Args:
        resume_id (int): ID du résumé à modifier.
        resume (ResumeRequest): Nouvelles données du résumé.

    Returns:
        dict: Statut de succès et message.
    """
    result = update_resume_by_id(
        resume_id=resume_id,
        data={"name": resume.name, "text": resume.text, "user_id": resume.user_id}
    )

    if result:
        return {"success": True, "message": "Résumé modifié"}
    else:
        return {"success": False, "message": "Une erreur est survenue"}

@app.get("/resume/{resume_id}")
def get_one_resume(resume_id: int):
    """Récupérer un résumé spécifique par son ID.

    Args:
        resume_id (int): ID du résumé à récupérer.

    Returns:
        dict: Statut de succès, message et données du résumé.
    """
    resume = get_resume_by_id(resume_id)
    print(resume)
    if resume == None:
        return {"success": False, "message": "Résumé introuvable"}

    return {"success": True, "data": ResumeResponse.model_validate(resume)}

@app.post("/add_resume/")
def add_resume(resume: ResumeRequest):
    """Créer un nouveau résumé pour un utilisateur.

    Args:
        resume (ResumeRequest): Informations du résumé à créer.

    Returns:
        dict: Statut de succès et message.
    """
    write_resume_db(
        user_id=resume.user_id,
        data=[{"name": resume.name, "text": resume.text}]
    )
    return {"success": True, "message": "Résumé ajouté et Summary mis à jour"}


@app.delete("/delete_user/{user_id}")
def delete_user(user_id: int):
    """Supprimer un utilisateur et tous ses résumés associés.

    Args:
        user_id (int): ID de l'utilisateur à supprimer.

    Returns:
        dict: Statut de succès et message.
    """
    if delete_user_db(user_id):
        return {"success": True, "message": "L'utilisateur a été supprimé avec succès"}
    else:
        return {"success": False, "message": "L'utilisateur n'existe pas"}

@app.delete("/delete_resume/{resume_id}")
def delete_resume(resume_id: int):
    """Supprimer un résumé spécifique par son ID.

    Args:
        resume_id (int): ID du résumé à supprimer.

    Returns:
        dict: Statut de succès et message.
    """
    if delete_resume_by_user_db(resume_id):
        return {"success": True, "message": "Le résumé a été supprimé avec succès"}
    else:
        return {"success": False, "message": "Le résumé n'a pas pu être supprimé"}

@app.get("/get_resume/{user_id}")
def get_resume_by_user_id(user_id: int):
    """Récupérer tous les résumés d'un utilisateur.

    Args:
        user_id (int): ID de l'utilisateur.

    Returns:
        dict: Statut de succès, liste des résumés ou message d'erreur.
    """
    try:
        df = read_resume_by_user_id(user_id)

        # Conversion du DataFrame en liste de dictionnaires
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
    """Authentifier un utilisateur avec son pseudo et mot de passe.

    Args:
        user (UserRequest): Identifiants de connexion (pseudo et mot de passe).

    Returns:
        dict: Statut de succès, message et données de l'utilisateur si authentifié.
    """
    # Recherche de l'utilisateur par pseudo
    user_found = find_user_by_pseudo(user.pseudo)

    if not user_found:
        return {"success": False, "message"  : "Pseudo ou mot de passe incorrect "} 
 

    # Vérification du mot de passe avec bcrypt
    if bcrypt.checkpw(user.password.encode('utf-8'), user_found.password.encode('utf-8')):
        return {
            "success": True,
            "message": "Vous êtes bien connecté",
            "data": UserResponse.model_validate(user_found)
        }

    return {"success": False, "message": "Pseudo ou mot de passe incorrect"}



if __name__ == "__main__":
    # Lancement du serveur pour le développement
    uvicorn.run(
        "apis.data_api.core_api:app",  # Chemin vers le module de l'application
        host="127.0.0.1",
        port=8001,
        reload=False  # Recharge automatique pour le dev, à désactiver en prod
    )