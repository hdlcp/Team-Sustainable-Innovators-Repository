from app.commons.instances.instances import logger
from app.data.entities.donnees.donnees import Donnees
from app.data.entities.dispositif.dispositif import Dispositif
from app.data.entities.config.entities_config import db
from datetime import datetime

class DonneesAdaptater:
    @staticmethod
    def create_donnees(data) -> Donnees:
        try:
            nouvelles_donnees = Donnees()
            nouvelles_donnees.from_dict(data)
            db.session.add(nouvelles_donnees)
            db.session.commit()
            return nouvelles_donnees
        except Exception as e:
            logger.error(f"Error creating donnees: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def get_donnees_by_dispositif(dispositif_id: int) -> Donnees:
        try:
            return Donnees.query.filter_by(dispositif_id=dispositif_id).order_by(Donnees.created_at.desc()).first()
        except Exception as e:
            logger.error(f"Error fetching donnees by dispositif: {e}")
            return None

    @staticmethod
    def get_historique_donnees(page: int, per_page: int, dispositif_id: int = None, date_debut: str = None, date_fin: str = None):
        try:
            query = Donnees.query
            
            if dispositif_id:
                query = query.filter_by(dispositif_id=dispositif_id)
            
            if date_debut:
                query = query.filter(Donnees.created_at >= datetime.fromisoformat(date_debut))
            
            if date_fin:
                query = query.filter(Donnees.created_at <= datetime.fromisoformat(date_fin))
            
            return query.order_by(Donnees.created_at.desc()).paginate(page=page, per_page=per_page)
        except Exception as e:
            logger.error(f"Error fetching historique donnees: {e}")
            return None

    @staticmethod
    def get_dispositif_by_id(dispositif_id: int) -> Dispositif:
        try:
            return Dispositif.query.get(dispositif_id)
        except Exception as e:
            logger.error(f"Error fetching dispositif: {e}")
            return None 