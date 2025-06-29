import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate
from app.commons.config.config.config import Config
from app.commons.config.errors.errors import register_error_handlers
from app.core.blueprint.blueprint import initialize_blueprint_route
from app.data.entities.config.entities_config import db

# Initialisation de JWT
jwt = JWTManager()

def create_app():
    """Create and configure the Flask application."""
    # Obtenir le chemin absolu du dossier static
    static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'static'))
    
    app = Flask(__name__, 
                static_folder=static_folder,
                static_url_path='/static')

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('data_base_uri', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    
    print(f"Connecting to database: {app.config['SQLALCHEMY_DATABASE_URI']}")

    
    # Configuration email
    app.config['MAIL_SERVER'] = os.getenv('smtp_server', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('smtp_port', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('smtp_user', '')
    app.config['MAIL_PASSWORD'] = os.getenv('smtp_password', '')

    # Initialiser les extensions avec l'application
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers=["Authorization", "Content-Type"])
    
    # Initialiser Flask-Migrate
    migrate = Migrate(app, db)
    
    # Configuration de Swagger
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    
    # Enregistrer les gestionnaires d'erreurs
    register_error_handlers(app)
    
    # Initialiser les routes
    initialize_blueprint_route(app)
    
    # Configurer Swagger UI
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "HydroNex API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    return app, migrate



