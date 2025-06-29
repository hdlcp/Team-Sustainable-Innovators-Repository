from flask import request
from app.commons.response.custom_response import CustomResponse
from app.adaptater.alerte_recommandation.alerte_recommandation_adaptater import AlerteRecommandationAdaptater
from app.commons.instances.instances import logger

def get_alertes():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        alertes = AlerteRecommandationAdaptater.get_all_alertes(
            page=page,
            per_page=per_page
        )
        if not alertes:
            return CustomResponse.error("Aucune alerte trouvée", 404)
        
        # Formater les résultats
        resultats = {
            'data': [alerte.to_dict() for alerte in alertes.items],
            'total': alertes.total,
            'page': page,
            'per_page': per_page
        }
        
        return CustomResponse.success("Alertes récupérées avec succès", resultats)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des alertes: {str(e)}")
        return CustomResponse.error(str(e), 500) 