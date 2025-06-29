from app.commons.instances.instances import logger
from app.data.entities.admin.admin import Admin
from app.data.entities.config.entities_config import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from datetime import datetime, timedelta

class AdminAdaptater:
    @staticmethod
    def authenticate(email: str, password: str) -> tuple[Admin, str]:
        try:
            admin = AdminAdaptater.get_admin_by_email(email)
            if not admin:
                return None, "Email non trouvé"
            
            if not admin.check_password(password):
                return None, "Mot de passe incorrect"
            
            token = AdminAdaptater.generate_token(admin)
            if not token:
                return None, "Erreur lors de la génération du token"
            
            return admin, token
        except Exception as e:
            logger.error(f"Error authenticating admin: {e}")
            return None, str(e)

    @staticmethod
    def check_email_exists(email: str) -> bool:
        try:
            return Admin.query.filter_by(email=email).first() is not None
        except Exception as e:
            logger.error(f"Error checking email existence: {e}")
            return False

    @staticmethod
    def create_admin(data) -> Admin:
        try:
            # Vérifier si l'email existe déjà
            if AdminAdaptater.check_email_exists(data['email']):
                return None

            admin = Admin()
            admin.from_dict(data)
            
            db.session.add(admin)
            db.session.commit()
            return admin
        except Exception as e:
            logger.error(f"Error creating admin: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def get_admin_by_email(email: str) -> Admin:
        try:
            return Admin.query.filter_by(email=email).first()
        except Exception as e:
            logger.error(f"Error fetching admin by email: {e}")
            return None

    @staticmethod
    def generate_token(admin: Admin) -> str:
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': admin.id
            }
            return jwt.encode(
                payload,
                os.getenv('JWT_SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            logger.error(f"Error generating token: {e}")
            return None

    @staticmethod
    def change_password(admin: Admin, new_password: str) -> bool:
        try:
            admin.set_password(new_password)
            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error changing password: {e}")
            db.session.rollback()
            return False 