from flask import request
from app.commons.response.custom_response import CustomResponse
from app.adaptater.chatbot.chatbot_adaptater import ChatbotAdaptater
from app.commons.instances.instances import logger

def chat():
    """Gère les interactions avec le chatbot"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return CustomResponse.error("Le message est requis", 400)
        
        message = data['message']
        
        # Instancier le chatbot
        chatbot = ChatbotAdaptater()
        response = chatbot.generate_response(message)
        
        return CustomResponse.success("Réponse du chatbot", {"response": response})
    except Exception as e:
        logger.error(f"Erreur lors de l'interaction avec le chatbot: {str(e)}")
        return CustomResponse.error(str(e), 500) 