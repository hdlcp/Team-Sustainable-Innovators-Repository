from datetime import datetime
from app.data.entities.config.entities_config import db

class Newsletter(db.Model):
    __tablename__ = 'newsletter'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)
    actif = db.Column(db.Boolean, default=True)

    def __init__(self, email: str, nom: str):
        self.email = email
        self.nom = nom
   
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'nom': self.nom,
            'date_inscription': self.date_inscription.isoformat() if self.date_inscription else None,
            'actif': self.actif
        }

    def from_dict(self, data):
        self.nom = data.get('nom', self.nom)
        self.email = data.get('email', self.email)
        return self
    