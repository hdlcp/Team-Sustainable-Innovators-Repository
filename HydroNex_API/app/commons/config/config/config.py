from datetime import timedelta
from app.commons.helpers.load_doten import Dotenv
class Config:
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///hydronex.db'  # Utilisation de SQLite
    SQLALCHEMY_DATABASE_URI = Dotenv.SQLALCHEMY_DATABASE_URI
    #psql -h localhost -U postgres -d "hydronex"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'hydronex_gaiathon_2025' 
    JWT_SECRET_KEY = 'hydronex_gaiathon_2025_jwt_key' 
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=3)

    SCHEDULER_API_ENABLED = True