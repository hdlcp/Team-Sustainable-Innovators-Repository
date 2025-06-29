from flask import Flask
from app.routes.donnees_routes import donnees_bp
from app.routes.dispositif_routes import dispositif_bp
from app.routes.chatbot_routes import chatbot_bp
from app.routes.newsletter_routes import newsletter_bp
from app.routes.alerte_routes import alerte_bp
from app.routes.auth_routes import auth_bp

def initialize_blueprint_route(app: Flask):
    """
    Initialise et enregistre tous les blueprints de l'application
    """
    # Enregistrement des blueprints avec leurs préfixes
    app.register_blueprint(donnees_bp, url_prefix='/api')
    app.register_blueprint(dispositif_bp, url_prefix='/api')
    app.register_blueprint(chatbot_bp, url_prefix='/api')
    app.register_blueprint(newsletter_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(alerte_bp, url_prefix='/api')


