from functools import wraps
from flask import request, jsonify
import jwt
import os
from app.commons.response.custom_response import CustomResponse

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Vérifier si le token est présent dans l'en-tête
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return CustomResponse.error("Token manquant ou invalide", 401)
        
        try:
            # Décoder le token
            data = jwt.decode(
                token,
                os.getenv('JWT_SECRET_KEY'),
                algorithms=['HS256']
            )
            # Ajouter l'ID de l'admin à la requête
            request.admin_id = data['sub']
        except jwt.ExpiredSignatureError:
            return CustomResponse.error("Token expiré", 401)
        except jwt.InvalidTokenError:
            return CustomResponse.error("Token invalide", 401)
        except Exception as e:
            return CustomResponse.error(str(e), 401)
        
        return f(*args, **kwargs)
    
    return decorated 