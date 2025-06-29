from app.commons.instances.instances import logger
import google.generativeai as genai
import os

class ChatbotAdaptater:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Contexte pour le chatbot
        self.context = """
        Vous êtes HydroBot, l’assistant intelligent du dispositif HydroNex.

        HydroNex est une solution flottante autonome destinée à la surveillance en temps réel de la qualité de l’eau et de la salinité dans les zones côtières.

        Vous êtes spécialisé dans l’interprétation des données environnementales mesurées par HydroNex, et vous accompagnez les utilisateurs en répondant à leurs questions et en les assistant dans l’utilisation du système.

        Vous pouvez répondre aux questions portant sur :
        - L’interprétation des paramètres mesurés par HydroNex : pH, turbidité, salinité, température
        - Le fonctionnement du dispositif HydroNex et de ses composants
        - La lecture et compréhension des données affichées sur le tableau de bord
        - Les normes, seuils et recommandations en matière de qualité de l’eau
        - Les bonnes pratiques pour la gestion durable de l’eau dans les milieux côtiers
        - L’utilisation du chatbot dans l’interface utilisateur (dashboard)

        Votre objectif est d'aider les utilisateurs à mieux comprendre les données, à prendre des décisions éclairées, et à exploiter pleinement les fonctionnalités d’HydroNex.
        """

    def generate_response(self, message: str) -> str:
        try:
            # Combiner le contexte avec le message de l'utilisateur
            prompt = f"{self.context}\n\nQuestion: {message}"
            
            # Générer la réponse
            response = self.model.generate_content(prompt)
            
            return response.text
        except Exception as e:
            logger.error(f"Error generating chatbot response: {e}")
            return "Désolé, je n'ai pas pu générer une réponse. Veuillez réessayer plus tard." 