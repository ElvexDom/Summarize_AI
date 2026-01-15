# Outils de gestion de la base de données SQLite avec SQLAlchemy
import pandas as pd
import os
from loguru import logger
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path
from typing import List, Union

# --- 1. Configuration des Chemins ---
# Chemin relatif vers le fichier de base de données
DB_FILE_PATH_RELATIVE = os.path.join("data", "DB.db")

# Détermination du répertoire racine du projet
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent  # Remonte au niveau projet

# Chemin absolu vers la base de données
DB_FILE_PATH = PROJECT_ROOT / DB_FILE_PATH_RELATIVE
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE_PATH.absolute()}"

# Création du moteur de base de données SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. Modèles de Données (ORM) ---
class Users(Base):
    """Modèle utilisateur contenant les informations d'authentification."""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pseudo = Column(String, unique=True)
    password = Column(String)
    summaries = relationship("Summary", back_populates="user", cascade="all, delete-orphan")


class Resume(Base):
    """Modèle représentant un résumé de texte."""
    __tablename__ = 'resume'
    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_name = Column(String)
    resume = Column(String)


class Summary(Base):
    """Modèle de liaison entre utilisateurs et résumés (table d'association)."""
    __tablename__ = 'summary'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ID_user = Column(Integer, ForeignKey(Users.id))
    ID_resume = Column(Integer, ForeignKey(Resume.id))
    user = relationship("Users", back_populates="summaries")


# --- 3. Fonctions d'Interface ---

def get_db_session() -> Session:
    """Crée et retourne une nouvelle session de base de données.

    Returns:
        Session: Session SQLAlchemy pour interagir avec la base de données.
    """
    return SessionLocal()

def write_user_db(data):
    """Enregistre un ou plusieurs utilisateurs dans la base de données.

    Args:
        data (Union[pd.DataFrame, List[dict]]): Données des utilisateurs.
            Les clés/colonnes attendues sont 'pseudo' et 'password'.

    Returns:
        bool: True si l'écriture a réussi, False en cas d'erreur (utilisateur déjà existant).
    """
    users_to_insert = []

    # Conversion vers List[dict]
    if isinstance(data, pd.DataFrame):
        logger.info("Conversion de l'entrée : DataFrame -> List[dict].")
        users_to_insert = data.reset_index().to_dict('records')

    elif isinstance(data, list):
        logger.info("Entrée traitée comme List[dict].")
        users_to_insert = data

    else:
        logger.error(f"Type de donnée non supporté pour write_db : {type(data)}")
        raise TypeError("write_db n'accepte que pd.DataFrame ou List[dict].")

    # Insertion dans la base de données
    db = get_db_session()
    try:
        for user_data in users_to_insert:
            pseudo = user_data.get('pseudo', '').strip()
            password = user_data.get('password', '').strip()

            # Nettoyage des champs
            if not pseudo:
                pseudo = "NULL_TEXT_EMPTY"
                logger.warning("Pseudo vide détecté, remplacé par 'NULL_TEXT_EMPTY'.")

            if not password:
                password = "NULL_TEXT_EMPTY"
                logger.warning("Mot de passe vide détecté, remplacé par 'NULL_TEXT_EMPTY'.")

            new_user = Users(
                pseudo=pseudo,
                password=password
            )

            db.add(new_user)

        db.commit()
        logger.success(f"Écriture de {len(users_to_insert)} utilisateur(s) dans la BDD réussie.")
        return True

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Erreur d'écriture dans la BDD : {e}")
        return False

    finally:
        db.close()

def update_resume_by_id(resume_id: int, data: dict):
    """Met à jour un résumé existant par son ID.

    Args:
        resume_id (int): ID du résumé à modifier.
        data (dict): Dictionnaire contenant les nouvelles données avec la clé 'text'.

    Returns:
        bool: True si la modification a réussi, False sinon.
    """
    if not isinstance(data, dict):
        logger.error(f"Type de donnée non supporté pour update_resume_by_id : {type(data)}")
        raise TypeError("update_resume_by_id n'accepte que dict.")

    db = get_db_session()
    try:
        # Récupération du résumé
        resume = db.query(Resume).filter(Resume.id == resume_id).first()

        if not resume:
            logger.warning(f"Résumé avec ID {resume_id} introuvable.")
            return False

        # Mise à jour du texte
        text = data.get("text", "").strip()
        name = data.get("name", "").strip()
        if not text:
            text = "NULL_TEXT_EMPTY"
            logger.warning("Texte du résumé vide détecté, remplacé par 'NULL_TEXT_EMPTY'.")

        resume.resume = text
        resume.resume_name = name
        db.flush()

        # Commit final
        db.commit()
        logger.success(f"Modification du résumé {resume_id} réussie.")
        return True

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Erreur de modification dans la BDD : {e}")
        return False

    finally:
        db.close()

def write_resume_db(user_id: int, data: Union[pd.DataFrame, List[dict]]):
    """Enregistre un ou plusieurs résumés pour un utilisateur et crée les liaisons dans Summary.

    Args:
        user_id (int): ID de l'utilisateur propriétaire des résumés.
        data (Union[pd.DataFrame, List[dict]]): Données des résumés.
            Les clés/colonnes attendues sont 'name' et 'text'.
    """
    resume_to_insert = []

    # Conversion vers List[dict]
    if isinstance(data, pd.DataFrame):
        logger.info("Conversion de l'entrée : DataFrame -> List[dict].")
        resume_to_insert = data.reset_index().to_dict('records')

    elif isinstance(data, list):
        logger.info("Entrée traitée comme List[dict].")
        resume_to_insert = data

    else:
        logger.error(f"Type de donnée non supporté pour write_resume_db : {type(data)}")
        raise TypeError("write_resume_db n'accepte que pd.DataFrame ou List[dict].")
    

    db = get_db_session()
    try:
        for resume_data in resume_to_insert:
            name = resume_data.get('name', '').strip()
            text = resume_data.get('text', '').strip()

            # Nettoyage des champs
            if not name:
                name = "NULL_TEXT_EMPTY"
                logger.warning("Nom de fichier vide détecté, remplacé par 'NULL_TEXT_EMPTY'.")
            if not text:
                text = "NULL_TEXT_EMPTY"
                logger.warning("Texte du résumé vide détecté, remplacé par 'NULL_TEXT_EMPTY'.")

            # Création du résumé
            new_resume = Resume(resume_name=name, resume=text)
            db.add(new_resume)
            db.flush()  # Récupère l'ID du résumé avant commit

            # Création de la liaison dans la table Summary
            new_summary = Summary(ID_user=user_id, ID_resume=new_resume.id)
            db.add(new_summary)

        # Commit final
        db.commit()
        logger.success(f"Insertion de {len(resume_to_insert)} résumé(s) et mise à jour de Summary réussie.")

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Erreur d'écriture dans la BDD : {e}")

    finally:
        db.close()

def get_resume_by_id(resume_id):
    """Récupère un résumé par son ID.

    Args:
        resume_id (int): ID du résumé à récupérer.

    Returns:
        Resume | None: Le résumé trouvé ou None si introuvable/ID invalide.
    """
    if not isinstance(resume_id, int):
        logger.warning(f"L'ID du résumé est incorrect (type: {type(resume_id)})")
        return None

    db = get_db_session()
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            logger.warning(f"Le résumé avec l'ID {resume_id} est introuvable")
            return None

        return resume
    finally:
        db.close()

def delete_user_db(user_id: int) -> bool:
    """Supprime un utilisateur et tous ses résumés associés via cascade.

    Args:
        user_id (int): ID de l'utilisateur à supprimer.

    Returns:
        bool: True si la suppression a réussi, False sinon.
    """
    db = get_db_session()
    try:
        # Vérification de l'existence de l'utilisateur
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            logger.warning(f"Utilisateur avec ID {user_id} introuvable.")
            return False

        # Suppression de l'utilisateur (cascade="all, delete-orphan" gère les Summary automatiquement)
        db.delete(user)
        logger.success(f"Utilisateur {user.pseudo} (ID: {user_id}) supprimé avec succès.")

        # Commit final
        db.commit()
        return True

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Erreur lors de la suppression de l'utilisateur {user_id} : {e}")
        return False

    finally:
        db.close()

def delete_resume_by_user_db(resume_id: int) -> bool:
    """Supprime un résumé et ses liaisons dans la table Summary.

    Args:
        resume_id (int): ID du résumé à supprimer.

    Returns:
        bool: True si la suppression a réussi, False sinon.
    """
    db = get_db_session()
    try:
        # Vérification de l'existence du résumé via Summary
        summary = db.query(Summary).filter(Summary.ID_resume == resume_id).first()
        if not summary:
            logger.warning(f"Résumé avec ID {resume_id} introuvable.")
            return False

        # Suppression des entrées dans Summary
        db.query(Summary).filter(Summary.ID_resume == resume_id).delete()
        logger.info(f"Suppression de la liaison Summary pour le résumé ID {resume_id}.")

        # Suppression du résumé
        db.query(Resume).filter(Resume.id == resume_id).delete()
        logger.info(f"Suppression du résumé avec ID {resume_id}.")

        # Commit final
        db.commit()
        return True

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Erreur lors de la suppression du résumé {resume_id} : {e}")
        return False

    finally:
        db.close()

def read_db() -> pd.DataFrame:
    """Lit tous les utilisateurs depuis la base de données.

    Returns:
        pd.DataFrame: DataFrame contenant les colonnes 'id', 'pseudo' et 'password'.
            Retourne un DataFrame vide avec les colonnes si aucun utilisateur n'existe.
    """
    db = get_db_session()
    try:
        all_users = db.query(Users).all()

        data = []
        for user in all_users:
            pseudo = user.pseudo
            mdp = user.password

            # Nettoyage à la lecture
            cleaned_pseudo = pseudo if pseudo else "NULL_TEXT_EMPTY"
            cleaned_mdp = mdp if mdp else "NULL_TEXT_EMPTY"

            data.append({
                'id': user.id,
                'pseudo': cleaned_pseudo,
                'password': cleaned_mdp
            })

        # Cas BDD vide
        if not data:
            return pd.DataFrame(columns=['id', 'pseudo', 'password']).set_index('id')

        return pd.DataFrame(data).set_index('id')

    except SQLAlchemyError as e:
        logger.error(f"Erreur de lecture dans la BDD : {e}")
        return pd.DataFrame(columns=['id', 'pseudo', 'password']).set_index('id')

    finally:
        db.close()

def read_resume_by_user_id(user_id: int) -> pd.DataFrame:
    """Lit tous les résumés associés à un utilisateur et renvoie un dictionnaire.

    Args:
        user_id (int): ID de l'utilisateur.

    Returns:
        dict: Dictionnaire contenant les clés 'id', 'resume_name' et 'resume'.
              Retourne un dictionnaire vide si aucun résumé n'existe.
    """
    db = get_db_session()
    try:
        summaries = (
            db.query(Resume)
            .join(Summary, Resume.id == Summary.ID_resume)
            .filter(Summary.ID_user == user_id)
            .all()
        )

        data = []
        for summary in summaries:
            id = summary.id
            name = summary.resume_name
            text = summary.resume

            # Nettoyage à la lecture
            cleaned_name = name if name else "NULL_TEXT_EMPTY"
            cleaned_text = text if text else "NULL_TEXT_EMPTY"

            data.append({
                'id' : id,
                'resume_name': cleaned_name,
                'resume': cleaned_text
            })

        return data if data else []

    except SQLAlchemyError as e:
        logger.error(f"Erreur de lecture des résumés pour l'utilisateur {user_id} : {e}")
        return []

    finally:
        db.close()

def find_user_by_pseudo(user_pseudo) -> Users | None:
    """Recherche un utilisateur par son pseudo.

    Args:
        user_pseudo (str): Pseudo de l'utilisateur à rechercher.

    Returns:
        Users | None: L'utilisateur trouvé ou None si introuvable.
    """
    db = get_db_session()
    try:
        user = db.query(Users).filter(Users.pseudo == user_pseudo).first()
        return user if user else None

    except SQLAlchemyError as e:
        logger.error(f"Erreur de lecture dans la BDD : {e}")
        return None

    finally:
        db.close()

def initialize_db():
    """Initialise la base de données en créant le dossier, le fichier SQLite et les tables.

    Cette fonction est idempotente : elle peut être appelée plusieurs fois sans effet néfaste.
    """
    # Création du dossier de données
    data_dir = DB_FILE_PATH.parent
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Dossier '{data_dir}' créé.")
    else:
        logger.info(f"Dossier '{data_dir}' déjà existant.")

    # Vérification de l'existence de la base de données
    if DB_FILE_PATH.exists():
        logger.info("La base de données SQLite existe déjà.")
    else:
        logger.info(f"Création de la base de données SQLite à : {DB_FILE_PATH}")

    # Création des tables (idempotent - ne recrée pas si elles existent)
    Base.metadata.create_all(bind=engine)
    logger.info("Les tables de la base de données ont été vérifiées/créées.")
