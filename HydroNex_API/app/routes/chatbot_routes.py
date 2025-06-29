from flask import Blueprint
from app.controllers.chatbot_controller import chat

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chat', methods=['POST'])
def chat_route():
    """
    Interagir avec le chatbot
    ---
    tags:
      - Chatbot
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - message
          properties:
            message:
              type: string
              description: Message à envoyer au chatbot
    responses:
      200:
        description: Réponse du chatbot générée avec succès
        schema:
          type: object
          properties:
            response:
              type: string
              description: Réponse du chatbot
      400:
        description: Message requis
      500:
        description: Erreur serveur
    """
    return chat() 