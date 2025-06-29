from app.commons.instances.instances import logger
from app.data.entities.newsletter.newsletter import Newsletter
from app.data.entities.config.entities_config import db

class NewsletterAdaptater:
    @staticmethod
    def create_subscriber(data: dict) -> Newsletter:
        try:
            subscriber = Newsletter(
                email=data['email'],
                nom=data['nom']
            )
            db.session.add(subscriber)
            db.session.commit()
            return subscriber
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'abonné: {str(e)}")
            db.session.rollback()
            return None

    @staticmethod
    def get_subscriber_by_email(email: str) -> Newsletter:
        try:
            return Newsletter.query.filter_by(email=email).first()
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'abonné: {str(e)}")
            return None

    @staticmethod
    def delete_subscriber(email: str) -> bool:
        try:
            subscriber = NewsletterAdaptater.get_subscriber_by_email(email)
            if subscriber:
                db.session.delete(subscriber)
                db.session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de l'abonné: {str(e)}")
            db.session.rollback()
            return False

    @staticmethod
    def get_all_subscribers():
        try:
            return Newsletter.query.all()
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des abonnés: {str(e)}")
            return []

    @staticmethod
    def get_all_emails():
        try:
            newsletters = Newsletter.query.all()
            return [newsletter.email for newsletter in newsletters]
        except Exception as e:
            logger.error(f"Error fetching newsletter emails: {e}")
            return [] 