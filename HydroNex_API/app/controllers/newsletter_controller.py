from flask import request
from app.commons.response.custom_response import CustomResponse
from app.adaptater.newsletter.newsletter_adaptater import NewsletterAdaptater
from app.services.smtp_function.send_mail import EmailService
from app.commons.instances.instances import logger

def subscribe():
    try:
        data = request.get_json()
        
        # Vérifier les champs requis
        if not data.get('email') or not data.get('nom'):
            return CustomResponse.error("Email et nom requis", 400)
        
        # Créer l'abonnement
        subscriber = NewsletterAdaptater.create_subscriber(data)
        if not subscriber:
            return CustomResponse.error("Erreur lors de l'inscription à la newsletter", 500)
        
        # Envoyer l'email de bienvenue avec le nouveau design
        email_service = EmailService()
        if not email_service.send_welcome_email(subscriber.email, subscriber.nom):
            logger.warning(f"Impossible d'envoyer l'email de bienvenue à {subscriber.email}")
        
        return CustomResponse.success("Inscription à la newsletter réussie", subscriber.to_dict())
    except Exception as e:
        logger.error(f"Erreur lors de l'inscription à la newsletter: {str(e)}")
        return CustomResponse.error(str(e), 500)

def unsubscribe():
    try:
        data = request.get_json()
        
        if not data.get('email'):
            return CustomResponse.error("Email requis", 400)
        
        if NewsletterAdaptater.delete_subscriber(data['email']):
            return CustomResponse.success("Désinscription de la newsletter réussie")
        else:
            return CustomResponse.error("Abonné non trouvé", 404)
    except Exception as e:
        logger.error(f"Erreur lors de la désinscription de la newsletter: {str(e)}")
        return CustomResponse.error(str(e), 500) 