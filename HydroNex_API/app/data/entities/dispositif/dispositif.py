from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from app.data.entities.config.entities_config import db
from flask import request

class Dispositif(db.Model):
    __tablename__ = 'dispositifs'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), unique=True, nullable=False)
    localisation = db.Column(db.String(200), unique=True, nullable=False)
    statut = db.Column(db.String(20), nullable=False)  # 'actif' ou 'inactif'
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    # Relations
    donnees = db.relationship('Donnees', backref='dispositif', lazy=True)
    alertes = db.relationship('Alerte_Recommandation', backref='dispositif', lazy=True, cascade='all, delete-orphan')
   
    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "localisation": self.localisation,
            "statut": self.statut,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def from_dict(self, data):
        self.nom = data.get('nom', self.nom)
        self.localisation = data.get('localisation', self.localisation)
        self.statut = data.get('statut', self.statut)
        return self
