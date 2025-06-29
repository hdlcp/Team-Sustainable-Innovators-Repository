from app.commons.instances.instances import logger
from app.data.entities.alerte_recommandation.alerte_recommandation import Alerte_Recommandation
from app.data.entities.config.entities_config import db

class AlerteRecommandationAdaptater:
    @staticmethod
    def create_alerte(data):
        try:
            nouvelle_alerte = Alerte_Recommandation()
            nouvelle_alerte.from_dict(data)
            db.session.add(nouvelle_alerte)
            db.session.commit()
            return nouvelle_alerte
        except Exception as e:
            logger.error(f"Error creating alerte: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def get_all_alertes(page=1, per_page=10):
        try:
            return Alerte_Recommandation.query.order_by(
                Alerte_Recommandation.created_at.desc()
            ).paginate(page=page, per_page=per_page)
        except Exception as e:
            logger.error(f"Error fetching alertes: {e}")
            return None 