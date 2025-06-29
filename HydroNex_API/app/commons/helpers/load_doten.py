from pathlib import Path
import os
from dotenv import load_dotenv
from app.commons.instances.instances import logger

# Chemin vers le fichier .env local
env_path = Path(__file__).resolve().parent.parent / 'const' / 'const' / '.env'

logger.info(f"[ENV] Recherche du fichier .env à : {env_path}")

if env_path.exists():
    load_dotenv(env_path)
    logger.info("[ENV] Fichier .env chargé avec succès.")
else:
    # Pas de .env : on est probablement en prod (Render)
    logger.warning(f"[ENV] Fichier .env non trouvé à {env_path} — utilisation des variables d’environnement système.")
    load_dotenv()  # Fallback au cas où il y a un .env ailleurs

class Dotenv:
    """Gestionnaire des variables d'environnement."""

    SMTPSERVEUR = os.getenv('smtp_server')
    SMTPPORT = int(os.getenv('smtp_port', 587))  # Valeur par défaut
    SMTPUSER = os.getenv('smtp_user')
    SMTPPASSWORD = os.getenv('smtp_password')
    SQLALCHEMY_DATABASE_URI = os.getenv('data_base_uri')
    GEMINI_API_KEY = os.getenv('gemini_api_key')
    COMPETITION_SECRET_KEY = os.getenv('competition_secret_key')
