from flask import Blueprint
from app.controllers.alerte_controller import get_alertes

alerte_bp = Blueprint('alerte', __name__)
 
# Route pour récupérer toutes les alertes
alerte_bp.route('/alertes', methods=['GET'])(get_alertes) 