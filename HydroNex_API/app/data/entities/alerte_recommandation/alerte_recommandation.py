from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from app.data.entities.config.entities_config import db
from flask import request

class Alerte_Recommandation(db.Model):
    __tablename__ = 'alertes_recommandations'

    id = db.Column(db.Integer, primary_key=True)
    dispositif_id = db.Column(db.Integer, db.ForeignKey('dispositifs.id'), nullable=False)
    alerte = db.Column(db.String(200), nullable=False)
    recommandation = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
   
    def to_dict(self):
        return {
            "id": self.id,
            "dispositif_id": self.dispositif_id,
            "alerte": self.alerte,
            "recommandation": self.recommandation,
            "created_at": self.created_at.isoformat(),
        }

    def from_dict(self, data):
        self.dispositif_id = data.get('dispositif_id', self.dispositif_id)
        self.alerte = data.get('alerte', self.alerte)
        self.recommandation = data.get('recommandation', self.recommandation)
        return self
    