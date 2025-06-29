from flask import jsonify, request
from app.data.entities.admin.admin import Admin
from app.data.entities.config.entities_config import db
import jwt
import os
from datetime import datetime, timedelta
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_jwt_extended import create_access_token
from app.commons.response.custom_response import CustomResponse
from app.adaptater.admin.admin_adaptater import AdminAdaptater
from app.services.smtp_function.send_mail import EmailService
from app.commons.instances.instances import logger

def generate_token(admin_id):
    """Génère un token JWT pour l'administrateur"""
    payload = {
        'admin_id': admin_id,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token valide pendant 1 jour
    }
    return jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')

def send_admin_credentials_email(admin_email, password):
    """Envoie les identifiants par email à l'administrateur"""
    try:
        # Configuration de l'email
        sender_email = os.getenv('SMTP_EMAIL')
        sender_password = os.getenv('SMTP_PASSWORD')
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT', 587))

        # Créer le message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = admin_email
        msg['Subject'] = "Vos identifiants HydroNex"

        # Corps du message
        body = f"""
        Bienvenue sur HydroNex !

        Vous avez été ajouté comme administrateur. Voici vos identifiants :

        Email : {admin_email}
        Mot de passe : {password}

        Veuillez changer votre mot de passe après votre première connexion.

        Cordialement,
        L'équipe HydroNex
        """

        msg.attach(MIMEText(body, 'plain'))

        # Envoyer l'email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {str(e)}")

def create_admin():
    """Crée un nouvel administrateur"""
    try:
        data = request.get_json()
        email = data.get('email')

        # Vérifier si l'email existe déjà
        if AdminAdaptater.check_email_exists(email):
            return CustomResponse.error("Cet email est déjà utilisé", 400)

        # Créer le nouvel administrateur
        admin = AdminAdaptater.create_admin(data)
        if not admin:
            return CustomResponse.error("Erreur lors de la création de l'administrateur", 500)

        # Envoyer l'email de bienvenue avec le nouveau design
        email_service = EmailService()
        if not email_service.send_admin_welcome_email(email, data.get('password')):
            logger.warning(f"Impossible d'envoyer l'email de bienvenue à {email}")

        return CustomResponse.success("Administrateur créé avec succès", admin.to_dict())
    except Exception as e:
        db.session.rollback()
        return CustomResponse.error(str(e), 500)

def login():
    try:
        data = request.get_json()
        
        # Vérifier les champs requis
        if not data.get('email') or not data.get('password'):
            return CustomResponse.error("Email et mot de passe requis", 400)
        
        # Vérifier les identifiants
        admin, token = AdminAdaptater.authenticate(data['email'], data['password'])
        if not admin:
            return CustomResponse.error(token, 401)
        
        return CustomResponse.success("Connexion réussie", {
            "token": token,
            "admin": admin.to_dict()
        })
    except Exception as e:
        return CustomResponse.error(str(e), 500)

def change_password():
    """Change le mot de passe d'un administrateur"""
    try:
        data = request.get_json()
        email = data.get('email')
        new_password = data.get('new_password')

        if not email or not new_password:
            return CustomResponse.error("Email et nouveau mot de passe requis", 400)

        # Mettre à jour le mot de passe
        admin = AdminAdaptater.update_password(email, new_password)
        if not admin:
            return CustomResponse.error("Administrateur non trouvé", 404)

        return CustomResponse.success("Mot de passe modifié avec succès")
    except Exception as e:
        db.session.rollback()
        return CustomResponse.error(str(e), 500) 