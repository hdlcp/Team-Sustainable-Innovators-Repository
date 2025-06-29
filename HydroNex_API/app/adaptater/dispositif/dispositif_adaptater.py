from app.commons.instances.instances import logger
from app.data.entities.dispositif.dispositif import Dispositif
from app.data.entities.config.entities_config import db

class DispositifAdaptater:
    @staticmethod
    def create_dispositif(data) -> Dispositif:
        try:
            dispositif = Dispositif()
            dispositif.from_dict(data)
            db.session.add(dispositif)
            db.session.commit()
            return dispositif
        except Exception as e:
            logger.error(f"Error creating dispositif: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def update_dispositif(dispositif_id: int, data) -> Dispositif:
        try:
            dispositif = Dispositif.query.get(dispositif_id)
            if not dispositif:
                return None
            
            dispositif.from_dict(data)
            db.session.commit()
            return dispositif
        except Exception as e:
            logger.error(f"Error updating dispositif: {e}")
            db.session.rollback()
            return None

    @staticmethod
    def get_dispositif_by_id(dispositif_id: int) -> Dispositif:
        try:
            return Dispositif.query.get(dispositif_id)
        except Exception as e:
            logger.error(f"Error fetching dispositif: {e}")
            return None

    @staticmethod
    def get_all_dispositifs():
        try:
            return Dispositif.query.all()
        except Exception as e:
            logger.error(f"Error fetching all dispositifs: {e}")
            return None

    @staticmethod
    def check_nom_exists(nom: str) -> bool:
        try:
            return Dispositif.query.filter_by(nom=nom).first() is not None
        except Exception as e:
            logger.error(f"Error checking nom existence: {e}")
            return False

    @staticmethod
    def check_localisation_exists(localisation: str) -> bool:
        try:
            return Dispositif.query.filter_by(localisation=localisation).first() is not None
        except Exception as e:
            logger.error(f"Error checking localisation existence: {e}")
            return False 