
from adaptater.user.user_adaptater  import UserAdaptater, User
from commons.const.string.app_string import AppString
from services.smtp_function.send_mail import EmailService

email_service = EmailService()
class UserUseCase :
    @staticmethod 
    def forgot_password( email):
        # Recherche de l'utilisateur par email
        user = UserAdaptater.get_user_by_email(email)
        
        if user:
            # Générer un code de réinitialisation sécurisé (par exemple, un token)
            reset_code = UserAdaptater.generate_reset_code(user)

            reset_link = f"{AppString.front_url}{reset_code}"

            # Préparation de l'email de réinitialisation
            subject = "Réinitialisation de mot de passe"
            message = f"""
            <p><strong>Bonjour {user.first_name},</strong></p>
            <p>Si vous êtes sur le web, veuillez cliquer sur le lien ci-dessous pour procéder à la réinitialisation :</p>
            <div style="text-align: center;">
            <p><a href="{reset_link}" style="color: #F68D04FF; font-weight: bold;">Réinitialiser mon mot de passe</a></p>
            </div>
            <p>Si vous utilisez l'application mobile, veuillez entrer le code suivant :</p>
            <div style="text-align: center;">
            <p style="color: #F68D04FF; font-weight: bold;">{reset_code}</p>
            </div>
            <p>Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer cet e-mail en toute sécurité.</p>"""
            # Tentative d'envoi de l'email
            if email_service.send_email(user.email, subject, message):
                return reset_code

        # Retourner None si l'utilisateur n'est pas trouvé ou en cas d'échec
        return None
    
    @staticmethod 
    def resent_user_link_for_forgot_password( email):
        # Recherche de l'utilisateur par email
        user = UserAdaptater.get_user_by_email(email)

        if user:  
            # Générer un code de vérification
            verification_code = UserAdaptater.generate_reset_code(user)
   
            verification_link = f"{AppString.front_url}{verification_code}"

            # Préparer l'email de vérification
            subject = "Renvoi de votre lien de réinitialisation pour mot de passe"
            message = f"""
            <p><strong>Bonjour {user.first_name},</strong></p>
            <p>Vous avez demandé la réinitialisation de votre mot de passe. Veuillez cliquer sur le lien ci-dessous pour procéder à la réinitialisation :</p>
            <div style="text-align: center;">
            <p><a href="{verification_link}" style="color: #F68D04FF; font-weight: bold;">Réinitialiser mon mot de passe</a></p>
            </div>
            <p>Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer cet e-mail en toute sécurité.</p>"""
            # Envoyer l'email avec le lien de vérification
            if email_service.send_email(user.email, subject, message):
                return verification_link  
            else:
                raise Exception("Échec de l'envoi de l'email de vérification")

        return None  
    

    @staticmethod
    def send_verification_code(user: User):
        # Générer un code de vérification
        verification_code = UserAdaptater.get_verification_code(user)

        # Préparer l'email de bienvenue et de vérification
        subject = "Bienvenue sur notre plateforme !"
        message = f"""
        <p><strong>Bonjour {user.first_name} {user.last_name},</strong></p>
        <p>Bienvenue sur notre plateforme ! Nous sommes ravis de vous compter parmi nos utilisateurs.</p>
        <p>Avant de commencer, veuillez vérifier votre compte avec le code ci-dessous :</p>
        <div style="text-align: center;">
        <strong style="color: blue; font-size: 28px;">{verification_code}</strong>
        </div>
        <p>Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer cet e-mail en toute sécurité.</p>
        <p>Merci de faire partie de notre communauté !</p>
        """

        
        # Envoyer l'email avec le lien de vérification
        if email_service.send_email(user.email, subject, message):
            return verification_code  

        return verification_code
