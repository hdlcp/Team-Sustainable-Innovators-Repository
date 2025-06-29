from flask import Blueprint
from app.controllers.auth_controller import (
    create_admin,
    login,
    change_password
)

auth_bp = Blueprint('auth', __name__)

# Route pour créer un nouvel administrateur
@auth_bp.route('/auth/register', methods=['POST'])
def register_route():
    return create_admin()

# Route pour l'authentification
@auth_bp.route('/auth/login', methods=['POST'])
def login_route():
    return login()

# Route pour changer le mot de passe
@auth_bp.route('/auth/change-password', methods=['POST'])
def change_password_route():
    return change_password()
 