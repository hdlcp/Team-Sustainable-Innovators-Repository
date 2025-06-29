from app.commons.instances.instances import logger
from app.data.entities.alerte_recommandation.alerte_recommandation import Alerte_Recommandation
from app.data.entities.config.entities_config import db

class AlerteAdaptater:
    @staticmethod
    def create_alerte(dispositif_id: int, alerte: str, recommandation: str) -> Alerte_Recommandation:
        try:
            nouvelle_alerte = Alerte_Recommandation(
                dispositif_id=dispositif_id,
                alerte=alerte,
                recommandation=recommandation
            )
            db.session.add(nouvelle_alerte)
            db.session.commit()
            return nouvelle_alerte
        except Exception as e:
            logger.error(f"Error creating alerte: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def get_alertes_by_dispositif(dispositif_id: int):
        try:
            return Alerte_Recommandation.query.filter_by(dispositif_id=dispositif_id).order_by(Alerte_Recommandation.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error fetching alertes by dispositif: {e}")
            return None

    @staticmethod
    def get_all_alertes():
        try:
            return Alerte_Recommandation.query.order_by(Alerte_Recommandation.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error fetching all alertes: {e}")
            return None 