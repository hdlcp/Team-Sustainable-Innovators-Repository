from flask_migrate import migrate, upgrade, init
from app.commons.instances.instances import logger
import os

def run_migrations(app):
    """Exécute les migrations de la base de données"""
    try:
        # Vérifier si le répertoire de migrations existe
        migrations_dir = 'migrations'
        if not os.path.exists(migrations_dir):
            logger.info("Initialisation du répertoire de migrations...")
            init()
            logger.info("Répertoire de migrations initialisé avec succès.")
        
        # Générer les scripts de migration
        logger.info("Génération des scripts de migration...")
        migrate()
        logger.info("Scripts de migration générés avec succès.")

        # Appliquer les migrations
        logger.info("Application des migrations...")
        upgrade()
        logger.info("Migrations appliquées avec succès.")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution des migrations : {str(e)}")
        raise e