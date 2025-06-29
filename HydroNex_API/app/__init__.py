from dotenv import load_dotenv
import os
from pathlib import Path
from app.commons.migrations_init.migrate_app import run_migrations
from app.core.dependance.dependance import create_app
from app.data.entities.config.entities_config import db

# Détection du contexte : LOCAL ou RENDER
env_path = Path(__file__).resolve().parent.parent / 'commons' / 'const' / 'const' / '.env'

if env_path.exists():
    load_dotenv(dotenv_path=env_path)  # En local
else:
    load_dotenv()  # En prod (Render lit les variables injectées automatiquement)

# Créer l'application et initialiser les migrations
app, migrate = create_app()

# Créer les tables et exécuter les migrations
with app.app_context():
    try:
        run_migrations(app)
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base de données : {str(e)}")
        raise e

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
