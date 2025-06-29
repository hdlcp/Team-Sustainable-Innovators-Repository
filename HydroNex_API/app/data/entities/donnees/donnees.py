from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from app.data.entities.config.entities_config import db
from flask import request

class Donnees(db.Model):
    __tablename__ = 'donnees'

    id = db.Column(db.Integer, primary_key=True)
    dispositif_id = db.Column(db.Integer, db.ForeignKey('dispositifs.id'), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    salinity = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=False)
    turbidity = db.Column(db.Float, nullable=False)
    battery_level = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    
   
    def to_dict(self):
        return {
            "id": self.id,
            "dispositif_id": self.dispositif_id,
            "temperature": self.temperature,
            "salinity": self.salinity,
            "ph": self.ph,
            "turbidity": self.turbidity,
            "battery_level": self.battery_level,
            "created_at": self.created_at.isoformat(),  
        }

    def from_dict(self, data):
        self.dispositif_id = data.get('dispositif_id', self.dispositif_id)
        self.temperature = data.get('temperature', self.temperature)
        self.salinity = data.get('salinity', self.salinity)
        self.ph = data.get('ph', self.ph)
        self.turbidity = data.get('turbidity', self.turbidity)
        self.battery_level = data.get('battery_level', self.battery_level)
        
        return self
    