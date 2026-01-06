# backend/modules/db_tools.py
import pandas as pd
import os
from loguru import logger
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from typing import List, Union


DataStorage = Union[pd.DataFrame, List[dict]]
# --- 1. Configuration des Chemins ---
# Chemin relatif de la BDD (comme spécifié par l'utilisateur)
DB_FILE_PATH_RELATIVE = os.path.join("data", "DB.db")

# Détermination du répertoire racine du projet pour obtenir un chemin absolu fiable
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent # Remonte de modules -> backend -> racine

# Chemin Absolu vers la BDD
DB_FILE_PATH = PROJECT_ROOT / DB_FILE_PATH_RELATIVE
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE_PATH.absolute()}" 
#Création de la base de données :
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. Modèle de Données (ORM) : La Classe Citation ---
class Users(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pseudo = Column(String)
    password = Column(String)
    summaries = relationship("Summary", back_populates="user")


class Resume(Base):
    __tablename__ = 'resume'
    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_name = Column(String)
    resume = Column(String)
   

class Summary(Base):
    __tablename__ = 'summary'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ID_user = Column(Integer, ForeignKey(Users.id))
    ID_resume = Column(Integer, ForeignKey(Resume.id))
    user = relationship("Users", back_populates="summaries") 
    
    
# --- 3. Fonctions d'Interface (Le Contrat) ---

def get_db_session() -> Session:
    """Fournit une session de BDD."""
    return SessionLocal()

def write_user_db(data):
    """
    Écrit des utilisateurs en base de données.
    Accepte une entrée de type pd.DataFrame ou List[dict].
    Les clés attendues sont : 'pseudo' et 'password'.
    """
    users_to_insert = []

    # --- SWITCH LOGIC: Conversion vers List[dict] ---
    if isinstance(data, pd.DataFrame):
        logger.info("Conversion de l'entrée : DataFrame -> List[dict].")
        users_to_insert = data.reset_index().to_dict('records')

    elif isinstance(data, list):
        logger.info("Entrée traitée comme List[dict].")
        users_to_insert = data

    else:
        logger.error(f"Type de donnée non supporté pour write_db : {type(data)}")
        raise TypeError("write_db n'accepte que pd.DataFrame ou List[dict].")

    # --- Insertion SQLAlchemy ---
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

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Erreur d'écriture dans la BDD : {e}")

    finally:
        db.close()

def write_resume_db(data):
    """
    Écrit des utilisateurs en base de données.
    Accepte une entrée de type pd.DataFrame ou List[dict].
    Les clés attendues sont : 'pseudo' et 'password'.
    """
    users_to_insert = []

    # --- SWITCH LOGIC: Conversion vers List[dict] ---
    if isinstance(data, pd.DataFrame):
        logger.info("Conversion de l'entrée : DataFrame -> List[dict].")
        users_to_insert = data.reset_index().to_dict('records')

    elif isinstance(data, list):
        logger.info("Entrée traitée comme List[dict].")
        users_to_insert = data

    else:
        logger.error(f"Type de donnée non supporté pour write_db : {type(data)}")
        raise TypeError("write_db n'accepte que pd.DataFrame ou List[dict].")

    # --- Insertion SQLAlchemy ---
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

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Erreur d'écriture dans la BDD : {e}")

    finally:
        db.close()


def read_db() -> pd.DataFrame:
    """
    Lit tous les utilisateurs depuis la BDD et les renvoie sous forme de DataFrame.
    Gère le cas de BDD vide en retournant un DataFrame vide avec les colonnes attendues.
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


def initialize_db():
    """
    Crée le dossier de données, la base SQLite et les tables si elles n'existent pas.
    """
    # 1. Création du dossier contenant la BDD
    data_dir = DB_FILE_PATH.parent
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Dossier '{data_dir}' créé.")
    else:
        logger.info(f"Dossier '{data_dir}' déjà existant.")

    # 2. Création / vérification de la base de données
    if DB_FILE_PATH.exists():
        logger.info("La base de données SQLite existe déjà.")
    else:
        logger.info(f"Création de la base de données SQLite à : {DB_FILE_PATH}")

    # 3. Création des tables
    Base.metadata.create_all(bind=engine)
    logger.info("Les tables de la base de données ont été vérifiées/créées.")
