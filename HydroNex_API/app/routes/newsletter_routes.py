from flask import Blueprint
from app.controllers.newsletter_controller import subscribe, unsubscribe

newsletter_bp = Blueprint('newsletter', __name__)

@newsletter_bp.route('/newsletter/subscribe', methods=['POST'])
def subscribe_route():
    """
    Inscription à la newsletter
    ---
    tags:
      - Newsletter
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - email
            - nom
          properties:
            email:
              type: string
              description: Email de l'abonné
            nom:
              type: string
              description: Nom de l'abonné
    responses:
      200:
        description: Inscription réussie
      400:
        description: Données invalides
      500:
        description: Erreur serveur
    """
    return subscribe()

@newsletter_bp.route('/newsletter/unsubscribe', methods=['POST'])
def unsubscribe_route():
    """
    Désinscription de la newsletter
    ---
    tags:
      - Newsletter
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - email
          properties:
            email:
              type: string
              description: Email de l'abonné
    responses:
      200:
        description: Désinscription réussie
      400:
        description: Données invalides
      404:
        description: Abonné non trouvé
      500:
        description: Erreur serveur
    """
    return unsubscribe() 